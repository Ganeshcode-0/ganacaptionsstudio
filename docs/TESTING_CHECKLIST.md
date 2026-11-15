# First end-to-end validation checklist

This checklist deliberately validates the caption pipeline before expanding the template collection. The JSON under `templates/` is a future template-schema preview/specification only; it is not a live template marketplace or a claim that all its effects render in the editor/export.

## 1. Configure provider credentials locally

1. Keep the repository root open (the folder containing `index.html` and `.env.example`).
2. Copy `.env.example` to a new file named `.env`.
3. Put your keys in that local `.env` file:

```env
GEMINI_API_KEY=your_real_gemini_key
SARVAM_API_KEY=your_real_sarvam_key
GEMINI_TRANSCRIBE_MODEL=gemini-3.5-transcribe
SARVAM_STT_MODEL=saaras:v4
```

4. Save and restart FastAPI. The backend loads the root `.env` file at startup.
5. Open `http://localhost:8000/api/health`. It should show `gemini_configured: true` and/or `sarvam_configured: true`. It must never return the key values.
6. Confirm `.env` is ignored by Git before committing. Commit `.env.example`, never `.env`.

For deployment, add the values as server-side Environment Variables in the hosting provider's project settings. Do not put keys in `index.html`, browser localStorage, a frontend `VITE_*` variable, screenshots, or GitHub. Redeploy/restart after changing variables. Only deploy the backend to a host that actually runs the Python API; a static-only deployment will not run FastAPI.

## 2. Test audio/transcription with a short known clip

Use a short video (5–20 seconds) with clear speech and its audio track. Note the exact spoken words and compare the output manually.

- [ ] Upload a video with audio and confirm it plays in the preview.
- [ ] Open Auto Captions and select the correct source language, then Auto detect.
- [ ] Test Gemini + Original transcript.
- [ ] Confirm the API response includes `timing: word` and word segments with start/end seconds. If it says `not_returned`, do not claim word-synced captions.
- [ ] Test Sarvam + Original transcript on a clip under 30 seconds.
- [ ] Confirm Sarvam segments are marked phrase-level, not word-level.
- [ ] Test Sarvam + Tenglish / Roman script and compare the transformed text with the preserved `original_text`.
- [ ] Test Sarvam + English translation separately; translation changes meaning-language, not just script.
- [ ] Correct a recognition error in the editor and confirm the edit remains when previewing.
- [ ] Check captions while playing from the start, middle, and end. Verify each segment appears only between its start/end times.
- [ ] Test a clip with silence, a pause, multiple sentences, and speech at the very end.
- [ ] Repeat with a real Telugu-English mixed clip; inspect proper nouns and code-mixed words.

Important provider constraints:
- Gemini 3.5 Transcribe supports word timestamps on prerecorded audio in VERBATIM mode; the feature is documented as experimental and can reduce transcription accuracy. The current backend uses the dedicated SDK configuration and must be verified with your API key and a real clip.
- Sarvam Saaras v4 REST supports files up to 30 seconds and phrase/chunk timestamps only. Its Batch API supports longer files (up to 2 hours) but also returns phrase/chunk timestamps, not per-word timestamps.
- Sarvam transliteration and translation are run as a separate output pass after preserving the original transcript. This uses an additional provider request.
- The current browser audio capture path is an initial testing path, not the final robust long-video media pipeline.

## 3. Verify the editor data and timing

- [ ] Word-level Gemini result creates one editable timed word segment per returned word.
- [ ] Sarvam result creates phrase segments only where provider timestamps exist.
- [ ] No timing is invented if the provider returns no timing.
- [ ] Editing a word/phrase changes only caption content, not the original source transcript.
- [ ] SRT export contains every timed segment in chronological order.
- [ ] Preview playback follows the same segment times as the timeline.
- [ ] Check that a word's timestamp is plausible against the audio waveform/audio itself.

## 4. Template JSON and export validation (later gate)

The existing JSON is a future-facing schema preview. Do not add dozens of templates yet. First prove the transcript/timing pipeline. Then use the same versioned template/style/animation model for preview and final renderer.

Before claiming a template works:
- [ ] Apply the template to real transcript segments with real provider timings.
- [ ] Change every editable word and phrase.
- [ ] Change font, size, position, fill, stroke, shadow and glow.
- [ ] Change entrance/exit animation and per-word emphasis.
- [ ] Add free text, edit it, move it and delete it.
- [ ] Render a short MP4 with original audio preserved.
- [ ] Compare the rendered file frame-by-frame with the preview for position, scale, timing, animation and font fallback.
- [ ] Confirm export is not a screen recording and does not depend on the browser tab remaining open.

## Current known gaps

This is not yet a production-ready full video editor. Burned-in MP4 rendering, a multi-track timeline, persistent projects, robust long-video/background transcription jobs, and a shared preview/export renderer are still future work. Do not treat SRT export as burned-in captions.
