# Gana Caption Studio — Product Vision

## Vision
Build a professional web-based caption-production studio for video creators, editors, agencies and social-media teams. A creator should be able to upload a video and complete the caption workflow in one place: transcribe, correct, time, format, design, animate, preview, export and reopen the project later.

Gana specialises in captions. It is not initially intended to replace full video editors such as Premiere Pro or After Effects.

## Product promise
**Comprehensive caption tools, accurate transcription, smooth editing and reliable exports.**

Success is measured by time saved, result accuracy, interaction responsiveness, export reliability and repeat usage—not by button or template count.

## Primary users
- Short-form creators publishing Reels, Shorts and TikToks.
- Podcast and interview editors.
- Freelance video editors.
- Agencies managing repeatable client styles.
- Educators and publishers creating accessible or multilingual videos.

Core job: turn spoken video into accurate, professionally designed captions and export a publish-ready video or subtitle file with minimal repetitive work.

## End-to-end workflow
1. Create a project and upload a video.
2. Validate the file, inspect metadata and extract audio.
3. Transcribe actual speech using a selected provider.
4. Review and correct the transcript.
5. Inspect and adjust word/phrase timing.
6. Generate caption blocks with configurable readability rules.
7. Apply a template or custom style.
8. Edit individual words, phrases and layers.
9. Position captions directly on the video canvas.
10. Adjust timing and clips in the timeline.
11. Preview the actual video and animation.
12. Export a burned-in video and/or subtitle files.
13. Save, reopen, duplicate or delete the project.

Every step presented as available must work. Never substitute fabricated transcripts, fake progress, sample exports or inert buttons for real functionality.

## Feature catalogue

### 1. Media and projects
- Drag-and-drop and file-picker upload.
- Upload progress, cancellation, retry and clear errors.
- File signature/type validation and size/duration limits.
- Detect resolution, aspect ratio, frame rate and duration.
- Audio extraction, thumbnails and waveform generation.
- Multiple media assets where supported.
- Replace media while retaining compatible caption data.
- Create, rename, duplicate, save, reopen and delete projects.
- Project recovery and export history.
- Private media storage and explicit retention/deletion policy.

Large video files must not be stored in localStorage. Keep media binaries in suitable storage and structured project data separately.

### 2. Transcription and transcript editing
- Actual speech-to-text transcription.
- Language selection/detection where reliable.
- Word-level timestamps when the provider returns and validates them.
- Phrase/segment timing when word timing is unavailable.
- Punctuation and capitalisation correction.
- Speaker labels only when supported and tested.
- Manual transcript correction, search/replace, split and merge.
- Optional filler-word identification.
- Custom vocabulary where supported.
- Retry and recoverable processing errors.
- Provider metadata and confidence information when available.

Never invent word timestamps or describe estimated timing as exact.

### 3. Language workflows
Evaluate Telugu script, Roman Telugu/Tenglish, Tamil, Malayalam, Hindi and English.

Keep these capabilities distinct:
- **Transcription:** recognise speech and produce text.
- **Transliteration:** represent the same spoken words in another writing system, such as Telugu script and Roman Telugu.
- **Translation:** convert meaning into another language.

Preserve the original transcript. Store transformed versions separately and keep them editable/reversible. Do not label transliteration as translation. Do not advertise a language before representative real-audio testing.

### 4. Caption composition and editing
- Generate caption blocks from transcript segments.
- Edit individual words and phrases.
- Split, merge, duplicate and delete blocks.
- Adjust start/end times and gaps.
- Group/ungroup words.
- Change line breaks and positioning.
- Set maximum lines, words and characters per line.
- Bulk-select and bulk-edit.
- Search/replace across a project.
- Copy/paste styles.
- Apply styles to a selection, track or project.
- Undo/redo and keyboard shortcuts.
- Autosave with visible saving/saved/error state.
- Detect overlaps, unusually long captions and captions outside media duration.

### 5. Timing and readability
- Configurable phrase grouping.
- Minimum/maximum duration and minimum gaps.
- Reading-speed guidance.
- Overlap detection.
- Align captions to speech.
- Pause-aware grouping.
- Safe-margin controls.
- Reflow line breaks after edits or canvas changes.
- Word highlighting only where accurate word timing exists.

Automated suggestions must be reviewable and reversible.

### 6. Typography and visual design
- Font family, weight, size and style.
- Letter spacing, line height and alignment.
- Fill colour, opacity and gradients.
- Stroke, shadow and background.
- Background opacity, padding and rounded corners.
- Glow, blur, shine and depth/extrusion where supported.
- Position, width, height, scale, rotation and anchor point.
- Safe-area overlays and alignment guides.
- Independent word and phrase styles.
- Multiple editable text/caption layers.

### 7. Word-level emphasis
- Select one or multiple words.
- Highlight/recolour selected words.
- Change size, weight, gradient or background per word.
- Karaoke-style highlighting.
- Per-word pop/scale emphasis.
- Save and reapply word-level presets.
- Retain word timing when changing appearance.

### 8. Animation
Initial families: fade, blur+fade, scale/pop, bounce, overshoot, slide/position, rotation, staggered word reveal, typewriter reveal, karaoke highlight, shine and glow.

Expose duration, intensity, easing and direction where meaningful. Preview and export must use the same animation definitions.

### 9. Templates and brand kits
Build template families over time: clean minimal, bold creator, cinematic kinetic typography, word-by-word, karaoke, neon/glow, gradient/3D, podcast/interview, educational, storytelling, multi-speaker and brand-specific.

Start with a small, genuinely distinct and tested library. A template is a reusable configuration—not a screenshot, duplicate name or one-off hard-coded component. Applying a template must not destroy transcript text or timing.

Brand kits may save fonts, colours, logos and preferred positioning.

### 10. Timeline
- Video/audio tracks and multiple caption/text tracks.
- Time ruler and playhead.
- Select, move, trim, split, merge and resize caption clips.
- Zoom and horizontal scroll.
- Multi-selection, snapping and track visibility/locking.
- Keyboard shortcuts.
- Correct clip-to-time mapping.
- Playback and scrubbing synchronised with captions.

Timeline edits must update project data, not just appearance.

### 11. Preview and export
Preview: persistent video element, accurate seeking/playback, supported aspect ratios, fit/zoom, frame stepping, full-screen, caption selection and direct editing. Preview quality must be independent of export quality.

Export: burned-in video with original audio, configurable resolution/frame rate/quality where supported, correct fonts/position/timing/animation, no editor-only controls, and subtitle formats such as SRT/VTT/ASS only when implemented and tested. Provide real progress/cancellation/retry where supported.

Do not call an export format supported until an actual output has been tested.

## Non-functional requirements
- Responsive editing interactions and stable memory use.
- Accurate transcript/caption timing.
- Preview/export consistency.
- Recoverable upload and processing failures.
- Secure isolation of user projects and media.
- Clear privacy and retention controls.
- No paid service or metered API without owner approval.
- Accessible controls, keyboard operation and useful errors.

## Initial boundaries
Focus on caption production. Full multitrack video editing, colour grading, compositing and general-purpose motion graphics are not initial goals unless customer demand validates them.

## Success metrics
Measure upload-to-first-usable-caption time, transcript correction time, time to style a video, bulk-edit time, export success/failure, timing correction rate, interaction frame times, dropped frames, cost per processed minute, completion and repeat usage. Never invent metrics or claim improvements before measurement.
