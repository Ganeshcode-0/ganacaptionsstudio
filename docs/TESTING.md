# Testing Strategy

## Principles
Test actual behaviour, not only appearance. Keep unit, integration, end-to-end, performance and security tests distinct. Use synthetic or properly licensed media. Never commit private customer videos, transcripts, credentials or exports. A feature is not complete until acceptance criteria pass.

## 1. Unit tests
- Caption timing and duration calculations.
- Transcript-to-caption grouping.
- Word/phrase segmentation.
- Line breaking/readability rules.
- Video/preview coordinate transforms.
- Timeline time-to-pixel conversion.
- Style and animation configuration validation.
- Undo/redo behaviour.
- Project schema validation and migrations.

## 2. Integration tests
- Upload and media metadata pipeline.
- Audio extraction.
- Transcription adapter and error mapping.
- Project persistence and reopen.
- Private media access and ownership checks.
- Caption editing and autosave.
- Render-job lifecycle.
- Subtitle generation.
- Export metadata and download authorisation.

Mock paid providers in ordinary CI. Run separately controlled provider integration tests only with explicit approval.

## 3. End-to-end scenario
1. Create a user and project.
2. Upload a test video.
3. Generate or load a verified test transcript.
4. Correct text and timing.
5. Apply a template.
6. Drag/resize a caption.
7. Move and trim a timeline block.
8. Save and reopen.
9. Export video and subtitle file.
10. Verify playback, duration, audio and captions.

## 4. Media matrix
Include short vertical, long vertical, landscape, square, high-resolution, supported codecs/containers, variable frame rate where relevant, silent/noisy audio, fast speech, multiple speakers, long speech and dense captions.

Before claiming language support, test representative Telugu-script, Roman Telugu/Tenglish workflow, Tamil, Malayalam, Hindi and English samples.

## 5. Interaction and coordinate tests
- Drag from text centre.
- Drag after preview zoom changes.
- Drag with letterboxing/pillarboxing.
- Drag at multiple viewport sizes.
- Resize from all supported handles.
- Rotate/change anchor point.
- Snapping on/off.
- Pointer leaves original element during drag.
- Pointer cancellation and Escape.
- Keyboard nudges.
- Inspector values remain synchronised.
- Saved coordinates persist after reopen.
- Export excludes handles/guides.

## 6. Timeline tests
Move/trim/split/merge blocks, multi-select, zoom/scroll, seek/playhead synchronisation, captions after the last speech segment, overlap prevention and frame/time rounding. Include a long project with many blocks.

## 7. Export verification
For every supported profile inspect file existence/size, container/codec, resolution/frame rate, duration, audio presence/synchronisation, caption timing/position, font/effect appearance, absence of editor overlays and playback in supported players.

## 8. Performance tests
Benchmark pointer-to-preview movement, resize/rotation, playhead, seeking/playback, timeline scrolling and dragging, style changes, dense projects, effects-heavy preview and long-running memory use.

Record browser, hardware, media characteristics, interaction frame times, dropped frames, long tasks and memory. Compare with a known baseline.

## 9. Security and data tests
- User A cannot read or modify User B's projects.
- User A cannot access User B's media or exports.
- Upload validation rejects disallowed content.
- Expired/revoked links stop working.
- Unauthorised render jobs are rejected.
- Secrets do not appear in source maps, bundles or logs.
- User deletion applies to assets under retention policy.
- Backup restoration is tested.

## 10. Release gates
Do not release with critical data-loss defects, failed cross-user isolation, unbounded upload processing, simulated primary workflows, unverified exports, unexplained severe performance regressions or undocumented skipped tests.

Publish passed, failed, skipped and unverified cases. Do not present targets as achieved results.
