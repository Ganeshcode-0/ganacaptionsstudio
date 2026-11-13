# Decision Log

Record material decisions affecting architecture, cost, security, user experience or maintainability. Add new entries at the top with date, status, context, options, decision and consequences.

## Open decisions

### D-001 — Confirm current frontend/backend stack
- Status: Open; audit required.
- Evidence needed: repository, dependencies, deployment and test status.
- Rule: do not migrate frameworks before confirming a measurable need.

### D-002 — Transcription provider
- Status: Open; compare candidates.
- Compare actual Telugu, Tamil, Malayalam, Hindi and English accuracy; timestamp quality; latency; file limits; reliability; data handling; cost per minute in INR; free tier and restrictions.
- Rule: use a provider adapter and server-side credentials. No paid activation without owner approval.

### D-003 — Video rendering/export engine
- Status: Open; benchmark required.
- Compare implementation fit, codecs, audio preservation, browser/device compatibility, render speed, effects support, deployment constraints and cost.
- Rule: validate actual exported files before choosing production path.

### D-004 — Project persistence and media storage
- Status: Open; inspect current Supabase configuration.
- Evaluate authentication, database, private object storage, row-level access control, quotas, backups, retention and egress cost.
- Rule: large media binaries do not belong in localStorage or ordinary project JSON.

### D-005 — Preview rendering technology
- Status: Open; benchmark required.
- Compare DOM/canvas/GPU-accelerated approaches for drag responsiveness, text quality, effects, coordinate correctness, browser compatibility and preview/export consistency.
- Rule: do not adopt a technology solely because it is fashionable.

### D-006 — Initial supported languages
- Status: Proposed scope; provider validation required.
- Evaluate Telugu script, Roman Telugu/Tenglish, Tamil, Malayalam, Hindi and English.
- Rule: distinguish transcription, transliteration and translation. Release only tested capabilities.

## Accepted product principles
- Gana specialises in caption production, not full general-purpose video editing.
- Accurate transcript/timing and smooth editing are foundational.
- Preview and export share semantic caption and animation definitions.
- Original media, transcript, caption content, appearance and editor-only controls remain separate.
- Customer media is private by default.
- No paid services or metered API activation without explicit owner approval.
- Performance claims require measurements.
- No mock data or simulated operation may be presented as a working feature.
