import os
from typing import Optional

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Gana Caption Studio API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:8000").split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

MAX_AUDIO_BYTES = 24 * 1024 * 1024
ALLOWED_AUDIO = {"audio/webm", "audio/mp4", "audio/mpeg", "audio/wav", "audio/x-wav", "audio/ogg", "audio/aac", "audio/mp3"}

@app.get("/api/health")
async def health():
    return {"ok": True, "service": "gana-caption-studio", "version": "0.1.0"}

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
        raise HTTPException(413, "Audio exceeds the 24 MB first-version limit. Use a shorter clip.")
    if mode not in {"transcribe", "translit", "translate", "native"}:
        raise HTTPException(400, "Unsupported caption output mode.")

    timeout = httpx.Timeout(120.0, connect=15.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        if provider == "gemini":
            key = os.getenv("GEMINI_API_KEY")
            if not key:
                raise HTTPException(503, "GEMINI_API_KEY is not configured on the server.")
            prompt = (
                "Transcribe the supplied speech accurately. Return only the transcript text, "
                "preserving the spoken language. Do not add commentary. "
                + ("Use Roman letters to transliterate the same words." if mode == "translit" else "")
                + ("Translate the spoken meaning into English." if mode == "translate" else "")
                + ("Use the selected language's native script." if mode == "native" else "")
                + (f" Speech language hint: {language}." if language != "auto" else "")
            )
            import base64
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {"inline_data": {"mime_type": content_type or "audio/webm", "data": base64.b64encode(audio).decode("ascii")}},
                    ]
                }]
            }
            model = os.getenv("GEMINI_TRANSCRIBE_MODEL", "gemini-3.5-transcribe")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            try:
                response = await client.post(url, params={"key": key}, json=payload)
                response.raise_for_status()
                body = response.json()
                text = "".join(p.get("text", "") for p in body.get("candidates", [{}])[0].get("content", {}).get("parts", []))
                if not text.strip():
                    raise ValueError("Gemini returned no transcript text.")
                return {"text": text.strip(), "provider": "gemini", "timing": "not_returned"}
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:600]
                raise HTTPException(exc.response.status_code, f"Gemini request failed: {detail}") from exc
            except (httpx.HTTPError, ValueError, KeyError, IndexError) as exc:
                raise HTTPException(502, f"Gemini transcription failed: {exc}") from exc

        if provider == "sarvam":
            key = os.getenv("SARVAM_API_KEY")
            if not key:
                raise HTTPException(503, "SARVAM_API_KEY is not configured on the server.")
            if mode == "translit":
                sarvam_mode = "translit"
            elif mode == "translate":
                sarvam_mode = "translate"
            elif mode == "native":
                sarvam_mode = "transcribe"
            else:
                sarvam_mode = "transcribe"
            data = {
                "model": os.getenv("SARVAM_STT_MODEL", "saaras:v4"),
                "mode": sarvam_mode,
                "with_timestamps": "false",
            }
            if language != "auto":
                data["language_code"] = language
            try:
                response = await client.post(
                    "https://api.sarvam.ai/speech-to-text",
                    headers={"api-subscription-key": key},
                    data=data,
                    files={"file": (file.filename or "audio.webm", audio, content_type or "audio/webm")},
                )
                response.raise_for_status()
                body = response.json()
                text = body.get("transcript") or body.get("text") or ""
                if not text.strip():
                    raise ValueError("Sarvam returned no transcript text.")
                return {"text": text.strip(), "provider": "sarvam", "timing": "phrase_or_provider_response"}
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:600]
                raise HTTPException(exc.response.status_code, f"Sarvam request failed: {detail}") from exc
            except (httpx.HTTPError, ValueError) as exc:
                raise HTTPException(502, f"Sarvam transcription failed: {exc}") from exc

    raise HTTPException(400, "Provider must be gemini or sarvam.")


# Serve the editor from the same origin so /api/transcribe works without CORS setup.
from fastapi.staticfiles import StaticFiles
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
app.mount("/", StaticFiles(directory=str(REPO_ROOT), html=True), name="editor")
