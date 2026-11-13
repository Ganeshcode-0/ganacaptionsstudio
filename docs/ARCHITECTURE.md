# Architecture Plan

## Status
This document defines boundaries and candidate responsibilities. It does not assert that a framework, database, renderer or provider has been selected. Confirm the existing implementation during the audit before migration.

## 1. Principles
- Preserve working code after understanding it.
- Separate interactive editor state from persisted project state.
- Separate media assets from transcript/caption metadata.
- Separate preview rendering from final export.
- Use replaceable transcription/rendering adapters.
- Keep long-running media operations out of the interactive UI thread.
- Authorise every project/media operation on the backend.
- Version project data and make migrations explicit.
- Make failures recoverable and jobs idempotent where possible.

## 2. Logical components

### Client/editor
Application shell, project manager, upload/media library, persistent video preview, caption overlay/transform controls, inspector, timeline/playhead, transcript workbench, template/animation browser and export status.

### Domain layer
Project model/versioning, media asset model, transcript and word timing model, caption tracks/blocks, text styles, animation configuration, template definitions, coordinate/time conversion, undo/redo commands and validation/readability rules.

### Backend/API
Authentication, project CRUD/ownership checks, upload authorisation, asset metadata, transcription jobs, provider adapters, render jobs, signed media access, export authorisation and usage/cost accounting.

### Background processing
Media probing, audio extraction, thumbnail/waveform generation, speech transcription, optional translation/transliteration, render/export and cleanup/retention jobs.

Use durable job infrastructure when required by the actual hosting architecture. Persist job state; do not rely on a browser tab remaining open.

## 3. Candidate data entities
- users
- projects
- media_assets
- transcription_jobs
- transcripts
- transcript_segments
- transcript_words
- caption_tracks
- caption_blocks
- text_layers
- style_presets
- animation_presets
- templates
- brand_kits
- render_jobs
- exports
- usage_events

Keep original transcript distinct from styled captions. Keep transcript timing distinct from timeline clip placement. Keep caption content distinct from typography. Editor selection handles are not export data. Export files are generated assets, not the source of truth.

## 4. Versioned project data
A validated project document should represent:
- Project ID and schema version.
- Source media ID and metadata.
- Canvas dimensions and aspect ratio.
- Transcript language and provider metadata.
- Transcript segments and optional word timings.
- Caption tracks and blocks.
- Per-word/per-phrase style overrides.
- Layer transforms in video-relative coordinates.
- Animation definitions and keyframes.
- Render configuration and project revision.

Keep large media binaries out of project JSON.

## 5. Coordinate and time model

### Video coordinate space
Store transforms relative to the video canvas, not browser screen pixels. Define origin, units, dimensions and anchor-point convention once.

### Preview conversion
Convert between video and screen coordinates while accounting for fit/zoom, letterboxing, aspect ratio, preview container size, device pixel ratio and browser scaling. Use the inverse transform for pointer dragging. Test multiple zoom and viewport sizes.

### Timeline time
Use one canonical internal time unit, such as integer microseconds or controlled milliseconds/frames, and convert only at rendering boundaries. Avoid floating-point drift. Frame-accurate operations must respect source/export frame rate.

## 6. Preview versus export
Both should consume the same semantic caption/style/animation model. Preview may use lower-quality rendering, caching or simplified effects for responsiveness but must preserve essential timing and geometry. Export uses final-quality rendering and omits editor controls.

Avoid separate hand-coded animation interpretations that diverge. Share effect definitions or a renderer contract and test both paths.

## 7. Provider adapters

### Transcription
A provider-neutral interface should cover job submission, status/result retrieval, segments, optional word timestamps, language metadata, retryable errors and usage/cost metadata. Provider secrets stay server-side.

### Rendering
A renderer boundary should cover input media/audio, caption project data, output format/dimensions, progress/cancellation, error details and output asset reference. Choose the renderer only after benchmarking actual codecs, audio preservation, browser/device support, performance and hosting cost.

## 8. Storage and database
Inspect the existing Supabase configuration before changing it. Supabase may suit authentication, relational metadata and private object storage, but actual configuration must be verified.

- Keep large binaries in object storage.
- Use private buckets/containers for customer media.
- Store object identifiers, not permanent public links.
- Generate short-lived signed access links after authorization.
- Apply backend ownership checks and row-level security where supported.
- Define quotas, retention and cleanup policies.

## 9. Observability
Track privacy-conscious events for upload, media probe, transcription, rendering, export, access denial and slow interaction failures. Use correlation IDs. Avoid logging transcript contents, raw media, credentials or signed URLs unnecessarily.

## 10. Decision gates
Before selecting/changing frontend framework, state library, canvas/DOM/GPU rendering, timeline implementation, transcription provider, rendering engine, hosting, queue or schema: audit the current project, benchmark candidates and record the decision in DECISIONS.md. Do not migrate for fashion.
