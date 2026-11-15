import asyncio
import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

app = FastAPI(title="Gana Caption Studio API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:8000").split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

MAX_AUDIO_BYTES = 24 * 1024 * 1024
ALLOWED_AUDIO = {
    "audio/webm", "audio/mp4", "audio/mpeg", "audio/wav",
    "audio/x-wav", "audio/ogg", "audio/aac", "audio/mp3",
}

def _seconds(value: Any) -> float | None:
    if value is None:
        return None
    if hasattr(value, "total_seconds"):
        return float(value.total_seconds())
    if isinstance(value, (int, float)):
        return float(value)
    raw = str(value).strip()
    if raw.endswith("s"):
        raw = raw[:-1]
    try:
        return float(raw)
    except ValueError:
        return None

def _gemini_words(response: Any) -> tuple[str, list[dict[str, Any]]]:
    transcript_parts: list[str] = []
    words: list[dict[str, Any]] = []
    for part in (getattr(response, "parts", None) or []):
        part_text = getattr(part, "text", None)
        audio_tx = getattr(part, "audio_transcription", None)
        tx_text = getattr(audio_tx, "text", None) if audio_tx else None
        if part_text:
            transcript_parts.append(str(part_text))
        elif tx_text:
            transcript_parts.append(str(tx_text))
        if audio_tx:
            for item in (getattr(audio_tx, "words", None) or []):
                word = getattr(item, "word", None)
                start = _seconds(getattr(item, "start_offset", None))
                end = _seconds(getattr(item, "end_offset", None))
                if word and start is not None and end is not None and end > start:
                    words.append({"text": str(word), "start": start, "end": end, "granularity": "word"})
    transcript = " ".join(x.strip() for x in transcript_parts if x.strip()).strip()
    if not transcript:
        transcript = str(getattr(response, "text", "") or "").strip()
    return transcript, words

def _sarvam_chunks(body: dict[str, Any]) -> list[dict[str, Any]]:
    ts = body.get("timestamps")
    if not isinstance(ts, dict):
        return []
    texts = ts.get("words") or []
    starts = ts.get("start_time_seconds") or []
    ends = ts.get("end_time_seconds") or []
    chunks = []
    for idx, text in enumerate(texts):
        if idx >= len(starts) or idx >= len(ends):
            break
        try:
            start, end = float(starts[idx]), float(ends[idx])
        except (TypeError, ValueError):
            continue
        if end > start and str(text).strip():
            chunks.append({"text": str(text).strip(), "start": start, "end": end, "granularity": "phrase"})
    return chunks

@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "service": "gana-caption-studio",
        "version": "0.2.0",
        "providers": {
            "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
            "sarvam_configured": bool(os.getenv("SARVAM_API_KEY")),
        },
    }

@app.post("/api/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    provider: str = Form("gemini"),
    language: str = Form("auto"),
    mode: str = Form("transcribe"),
):
    content_type = (file.content_type or "").split(";")[0].lower()
    if content_type not in ALLOWED_AUDIO and not content_type.startswith("audio/"):
        raise HTTPException(415, "The captured upload is not a supported audio file.")
    audio = await file.read(MAX_AUDIO_BYTES + 1)
    if not audio:
        raise HTTPException(400, "The audio file is empty.")
    if len(audio) > MAX_AUDIO_BYTES:
        raise HTTPException(413, "Audio exceeds the 24 MB first-version limit.")
    if mode not in {"transcribe", "translit", "translate", "native"}:
        raise HTTPException(400, "Unsupported caption output mode.")

    if provider == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise HTTPException(503, "GEMINI_API_KEY is not configured. Add it to the local .env file and restart the backend.")
        if mode != "transcribe":
            raise HTTPException(400, "Gemini word-timestamp mode currently supports original transcription only. Use Sarvam for transliteration or translation in this test build.")
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=key)
            config_args: dict[str, Any] = {"word_timestamp": True, "mode": "VERBATIM"}
            if language != "auto":
                config_args["language_codes"] = [language]
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=os.getenv("GEMINI_TRANSCRIBE_MODEL", "gemini-3.5-transcribe"),
                contents=[types.Part.from_bytes(data=audio, mime_type=content_type or "audio/webm")],
                config=types.GenerateContentConfig(
                    audio_transcription_config=types.AudioTranscriptionConfig(**config_args)
                ),
            )
            transcript, words = _gemini_words(response)
            if not transcript:
                raise ValueError("Gemini returned no transcript text.")
            return {
                "text": transcript,
                "original_text": transcript,
                "provider": "gemini",
                "language": language,
                "timing": "word" if words else "not_returned",
                "segments": words,
            }
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(502, f"Gemini transcription failed: {str(exc)[:500]}") from exc

    if provider == "sarvam":
        key = os.getenv("SARVAM_API_KEY")
        if not key:
            raise HTTPException(503, "SARVAM_API_KEY is not configured. Add it to the local .env file and restart the backend.")

        requested_mode = {"transcribe": "transcribe", "translit": "translit", "translate": "translate", "native": "transcribe"}[mode]
        timeout = httpx.Timeout(120.0, connect=15.0)

        async def sarvam_request(output_mode: str, with_timestamps: bool, language_code: str):
            data = {
                "model": os.getenv("SARVAM_STT_MODEL", "saaras:v4"),
                "mode": output_mode,
                "with_timestamps": "true" if with_timestamps else "false",
                "language_code": language_code,
            }
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    "https://api.sarvam.ai/speech-to-text",
                    headers={"api-subscription-key": key},
                    data=data,
                    files={"file": (file.filename or "audio.webm", audio, content_type or "audio/webm")},
                )
                response.raise_for_status()
                return response.json()

        try:
            # Preserve source-language text before any script conversion or translation.
            source_body = await sarvam_request("transcribe", False, language if language != "auto" else "unknown")
            original_text = str(source_body.get("transcript") or source_body.get("text") or "").strip()
            detected_language = source_body.get("language_code") or (language if language != "auto" else "unknown")
            if not original_text:
                raise ValueError("Sarvam returned no source transcript text.")

            output_body = await sarvam_request(requested_mode, True, detected_language)
            transcript = str(output_body.get("transcript") or output_body.get("text") or "").strip()
            if not transcript:
                raise ValueError("Sarvam returned no output transcript text.")
            segments = _sarvam_chunks(output_body)
            return {
                "text": transcript,
                "original_text": original_text,
                "provider": "sarvam",
                "language": output_body.get("language_code") or detected_language,
                "language_probability": output_body.get("language_probability"),
                "timing": "phrase" if segments else "not_returned",
                "segments": segments,
                "request_id": output_body.get("request_id"),
                "source_request_id": source_body.get("request_id"),
                "note": "Sarvam REST timestamps are phrase/chunk-level, not individual word-level.",
            }
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:500]
            raise HTTPException(exc.response.status_code, f"Sarvam request failed: {detail}") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise HTTPException(502, f"Sarvam transcription failed: {exc}") from exc

    raise HTTPException(400, "Provider must be gemini or sarvam.")

app.mount("/", StaticFiles(directory=str(REPO_ROOT), html=True), name="editor")
