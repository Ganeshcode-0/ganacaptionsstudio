# Development Roadmap

This is a proposed sequence, not a claim that any phase is implemented. Start with an audit of the actual application. A phase is complete only when its exit criteria pass.

## Phase 0 — Repository and product audit
- Inspect all source files, scripts, configuration and dependencies.
- Identify framework, build tooling and runtime.
- Classify working, incomplete, simulated and broken features.
- Inspect authentication, database, storage, APIs, upload, transcription, preview, timeline and export.
- Establish test coverage and performance baselines.
- Record security, data-loss, compatibility and cost risks.

**Exit:** verified architecture map, feature-status table, risk register and prioritised plan. Do not rewrite before the audit.

## Phase 1 — Repository foundation
- Add documentation, contribution guidance and environment examples.
- Add formatting, linting, type checking where appropriate and tests.
- Add CI checks and dependency/secret scanning where practical.
- Define development/production configuration.
- Never commit credentials, customer media or private exports.

**Exit:** reproducible setup, baseline checks and no committed secrets.

## Phase 2 — Editor shell and interaction engine
- Build/verify top toolbar, left tools, central preview, right inspector and bottom timeline.
- Keep the actual video element persistent.
- Implement caption selection, direct dragging, resize, rotation and snapping.
- Implement correct video-space coordinate conversion.
- Build real timeline operations.
- Add undo/redo, asynchronous autosave and performance instrumentation.

**Exit:** interactions are responsive on representative videos; coordinates persist after reopen and preview resizing.

## Phase 3 — Real media and transcription
- Securely upload real video assets.
- Extract audio and validate media metadata.
- Evaluate providers before selection.
- Implement server-side provider adapter.
- Generate real transcript text and provider-supported timestamps.
- Implement correction, split/merge and search.
- Store original transcript and provider metadata.
- Test target languages with real recordings.

**Exit:** a user can upload a video, receive actual transcript data, correct it and reopen the project.

## Phase 4 — Caption workbench and timing
- Convert transcript segments into caption blocks.
- Build phrase grouping and configurable line-breaking.
- Implement time editing, split/merge, bulk actions and readability checks.
- Add keyboard shortcuts.
- Keep transcript and caption timing data distinct.

**Exit:** users can prepare accurate captions without manually rebuilding every block.

## Phase 5 — Typography and templates
- Build editable typography properties.
- Support per-word and per-phrase styles.
- Build reusable template definitions and a small set of distinct styles.
- Add saved user presets and brand kits.
- Preserve transcript timing when styles change.

**Exit:** styles update the actual preview and persist correctly.

## Phase 6 — Animation engine
- Implement tested entrance, exit and emphasis effects.
- Add timing, intensity and easing.
- Add word-by-word and karaoke modes only where timestamps support them.
- Use shared definitions for preview and export.
- Profile expensive effects.

**Exit:** animation preview accurately represents export.

## Phase 7 — Rendering and export
- Select and validate rendering pipeline.
- Preserve source audio and synchronisation.
- Implement video and subtitle exports.
- Add background render jobs, progress, cancellation and retry where supported.
- Validate codec, resolution, frame rate, fonts, duration and effects.

**Exit:** representative exported files play correctly and match preview within documented tolerances.

## Phase 8 — Advanced creator productivity
- Translation and transliteration as separate workflows.
- Custom vocabulary and speaker tools.
- Batch formatting and bulk timing corrections.
- Advanced readability checks.
- More template families and animation presets.
- Team/agency workflows only after validating demand.

**Exit:** advanced tools demonstrably reduce repetitive editing time without harming reliability.

## Phase 9 — Controlled launch
- Test with a small group of real creators and editors.
- Fix critical/high-severity security and data-loss issues.
- Measure transcription and render cost per minute.
- Set upload/duration/usage limits based on capacity.
- Publish privacy, retention and deletion policies.
- Add error and usage monitoring.
- Validate willingness to pay before expanding infrastructure.

**Exit:** repeatable customer workflow, monitored costs, known limitations and support process.

## Prioritisation
1. Data integrity, security and reliable media handling.
2. Editor responsiveness and accurate coordinates.
3. Real transcription and timing.
4. Fast correction and bulk editing.
5. Typography and templates.
6. Animation.
7. Export reliability.
8. Advanced, less-frequently-used features.

Use GitHub issues for tasks and milestones for phases. This roadmap alone is not evidence that work is complete.
