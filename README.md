# Gana Caption Studio

A professional caption-production studio for video creators, editors, agencies and social-media teams.

## Product direction

Gana is focused on making the complete caption workflow fast, accurate and intuitive:

1. Upload a video and process its audio.
2. Generate and correct a real transcript.
3. Create accurately timed captions.
4. Style words, phrases and caption layers.
5. Animate captions and adjust them on a responsive timeline.
6. Preview and export the finished video or subtitle files.
7. Save projects and return to editing later.

The product should make caption-related work comprehensive without making the editor feel heavy.

## Product principles

- **Accuracy before decoration:** transcription and timing must be real and editable.
- **Direct manipulation:** users can select, drag, resize and position captions in the preview.
- **Responsive by design:** pointer movement, preview playback and timeline editing must remain smooth.
- **Preview/export consistency:** effects shown in the editor must render correctly in the final output.
- **Creator productivity:** bulk editing, reusable styles, keyboard shortcuts and smart caption formatting should save time.
- **Trust:** private media, secure project access, clear data retention and no hidden paid services.

## Documentation

- [Product vision and feature catalogue](docs/PRODUCT_VISION.md)
- [Development roadmap](docs/ROADMAP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Performance strategy](docs/PERFORMANCE.md)
- [Security plan](docs/SECURITY.md)
- [Testing strategy](docs/TESTING.md)
- [Decision log](docs/DECISIONS.md)

## Project status

The repository is being established. Implementation choices must be based on an audit of the actual existing application and its dependencies. Do not assume a framework, transcription provider, database schema or renderer before inspection.

## Non-goals

Gana is not initially intended to replace full video editors such as Premiere Pro or After Effects. Its primary focus is the caption-production workflow.

## Safety and cost

Never commit API keys, credentials, customer media or private exports. Do not enable paid infrastructure or metered APIs without explicit approval.
