# Performance Strategy

## Goal
Make direct manipulation, playback, scrubbing and timeline editing responsive even when projects contain many caption blocks and styled words. No universal zero-lag guarantee is possible across devices and media. Define measurable budgets, profile representative hardware and degrade gracefully without corrupting edits.

## 1. Initial targets
- Aim for 60 FPS visual interaction on supported desktop hardware.
- Keep pointer feedback responsive; avoid full-app updates per pointer event.
- Avoid avoidable long tasks on the main thread.
- Do not reload video for routine style/position changes.
- Avoid memory growth that scales uncontrollably with duration.
- Keep playback/timeline usable while background jobs run.

Measure median and 95th-percentile interaction frame times, dropped frames, long tasks and memory. Targets are not achieved results until measured.

## 2. Drag interaction pipeline
1. Capture pointer events and pointer identity.
2. Use pointer capture during a drag.
3. Keep temporary drag coordinates separate from persisted project data.
4. Schedule visual updates with requestAnimationFrame.
5. Update only the selected overlay/transform.
6. Avoid framework-wide updates for every pointer movement.
7. Avoid layout thrashing.
8. Use efficient transforms where suitable.
9. Commit one final project change on pointer release.
10. Create one undo command for the completed drag.
11. Queue autosave after commit, not for each pointer tick.

Handle pointer cancellation, lost capture, window blur, touch/pen input and Escape cancellation. Do not leave stale transform state.

## 3. Coordinate accuracy
- Store transforms in video-relative coordinates.
- Define one video canvas coordinate system.
- Account for fit, zoom, letterboxing, aspect ratio, device pixel ratio and browser scaling.
- Convert pointer coordinates using the inverse preview transform.
- Test multiple viewport sizes and zoom values.
- Keep inspector values synchronised with direct manipulation.

Smooth movement is unacceptable if the saved position is inaccurate.

## 4. Video preview
- Keep a persistent video element/source.
- Update overlays independently from video.
- Avoid reloading/re-decoding media for ordinary text changes.
- Avoid rendering the complete output video during interactive edits.
- Use adaptive preview quality if necessary.
- Keep final export quality independent.
- Avoid unnecessary canvas readbacks and expensive effects while dragging.
- Cache fonts, images and reusable effect resources.
- Release media resources when projects close.

Use acceleration only where benchmarking shows a benefit, with fallbacks.

## 5. Timeline
- Render visible tracks/clips efficiently; consider virtualization for long timelines.
- Isolate playhead updates from clip-list rendering.
- Avoid rebuilding all clips when one item moves.
- Batch ruler/marker work.
- Generate thumbnails and waveforms asynchronously.
- Cache waveform/thumbnail data.
- Cancel obsolete work when media or viewport changes.
- Derive clip positions from canonical time data.

## 6. Background processing
Consider workers/backend jobs for audio extraction, probing, waveform and thumbnail generation, transcription, large transcript transformations and export. Bound concurrency to avoid exhausting CPU, RAM, GPU or storage. Benchmark before adopting workers; they are not automatically faster.

Long-running jobs need persisted status, retry rules and clear failure states.

## 7. Effects and typography
Cache font and rendering resources. Avoid rebuilding text layout for unrelated changes. Do not stack costly blur/glow effects on every caption by default. Use simplified preview rendering only when essential appearance is preserved. Export must use intended final settings. Measure many simultaneously animated words.

## 8. Autosave and undo
Commit semantic commands, not pointer ticks. Coalesce repeated keyboard nudges where appropriate. Queue/debounce autosave. Handle out-of-order saves and network failures. Show saving/saved/failed states and preserve unsaved changes after transient errors.

## 9. Benchmarks
Maintain synthetic or properly licensed test assets for a short 9:16 clip, a longer video, high-resolution video, dense captions, multiple tracks and effects-heavy previews. Measure drag, resize, rotate, seek, playhead, clip move/trim, style changes, memory and export separately.

## 10. Acceptance record
For each benchmark record device/browser, video codec/resolution/frame rate/duration, number of caption blocks/layers, effect load, frame times, dropped frames, memory and reproduction steps. Fix bottlenecks; do not hide them by removing features or silently lowering output quality.
