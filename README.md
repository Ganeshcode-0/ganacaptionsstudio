# Gana Caption Studio

A caption-focused video editing workspace. The first implementation milestone delivers a real local video preview, live caption styling, selectable templates, canvas positioning, a single caption clip timeline, subtitle export and a server-side transcription adapter.

## Run locally

Requires Python 3.10+.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Add your API keys to .env on your own machine.
uvicorn backend.main:app --reload
```

Open http://localhost:8000. FastAPI serves both the editor and API from the same origin.

## First milestone capabilities

- Upload and preview a local video without uploading it to a server.
- Change 16:9, 9:16 and 1:1 preview canvas ratios.
- Apply five distinct caption design families without changing caption text.
- Edit text and typography, change colour and position, and drag the caption over the preview.
- Set a single caption layer's start/end time and scrub the video from the timeline.
- Export the current caption as an SRT subtitle file.
- Request speech transcription through the backend using Gemini or Sarvam.

## Important current limitations

- This is a **first vertical slice**, not the complete professional editor.
- The initial timeline has one video, audio and caption lane; it is not yet a multitrack editor.
- The current SRT export writes one caption block using the manually selected start/end times. It is not a word-aligned subtitle export.
- The current transcription endpoint returns transcript text only. It does not claim word-level timestamps. Caption timing must be reviewed/entered; do not treat estimated times as provider timings.
- Browser audio capture plays the video from the start to capture its audio. Short clips are recommended.
- Burned-in MP4 rendering, durable project storage, authentication, background jobs and cloud media storage are not implemented yet.
- Provider model IDs and API response shapes can change. Verify against the current provider account/docs before production use.

## Security

- Keep API keys in local `.env` or deployment environment variables.
- Never place API keys in frontend JavaScript, HTML, GitHub commits or browser storage.
- The sample API is not production-hardened: add authentication, rate limits, upload quotas, private media handling and strict CORS before public deployment.
