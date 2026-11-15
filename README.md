# Gana Caption Studio

A caption-focused video editing workspace. The first implementation milestone delivers a real local video preview, live caption styling, selectable templates, canvas positioning, a single caption clip timeline, subtitle export and a server-side transcription adapter.

## Run locally

Requires Python 3.10+.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and add your API keys. The backend loads it at startup.
uvicorn backend.main:app --reload
```

Open http://localhost:8000. FastAPI serves both the editor and API from the same origin.

## First milestone capabilities

- Upload and preview a local video without uploading it to a server.
- Preview the source video's original aspect ratio, switch to 16:9, 9:16 or 1:1, or enter a custom canvas size.
- Use the current five simple preview styles; the JSON in `templates/` is a future-facing schema preview, not a full template library.
- Edit text and typography, change colour and position, and drag the caption over the preview.
- Create multiple caption blocks, select/edit each block, split text, merge with the next block, delete blocks and adjust each block's start/end time.
- Drag captions horizontally/vertically on the preview and resize using the on-canvas handle or zoom controls.
- Adjust stroke, shadow and glow independently.
- Export timed caption blocks to SRT.
- Request speech transcription through the backend using Gemini or Sarvam, with provider timing granularity returned to the editor.

## Important current limitations

- This is a **first vertical slice**, not the complete professional editor.
- The initial timeline has one video, audio and caption lane with multiple caption blocks; it is not yet a multitrack editor.
- Gemini transcription is configured to request word-level timestamps in VERBATIM mode. The provider feature is experimental and must be verified with a real API-key test clip.
- Sarvam REST returns phrase/chunk-level timestamps, not word-level timestamps. The current UI creates timed blocks from the timestamps returned by the selected provider.
- If a provider returns no timestamps, the UI creates a manual full-clip caption block and explicitly marks timing as requiring review; it does not label that timing as AI-generated.
- Browser audio capture plays the video from the start to capture its audio. Short clips are recommended.
- Burned-in MP4 rendering, durable project storage, authentication, background jobs and cloud media storage are not implemented yet.
- Provider model IDs and API response shapes can change. Verify against the current provider account/docs before production use.

## Security

- Keep API keys in local `.env` or deployment environment variables.
- Never place API keys in frontend JavaScript, HTML, GitHub commits or browser storage.
- The sample API is not production-hardened: add authentication, rate limits, upload quotas, private media handling and strict CORS before public deployment.


## Provider configuration and validation

See [docs/TESTING_CHECKLIST.md](docs/TESTING_CHECKLIST.md) for safe API-key setup and a step-by-step Gemini/Sarvam test plan. The backend health endpoint reports whether each key is configured without exposing the key.

The JSON in `templates/premium-caption-templates.v1.json` is a future template schema preview only. It is not a separate live template library and its animations are not yet guaranteed in MP4 export.
