# Security and Privacy Plan

This is a requirements plan, not a security certification.

## 1. Threat model
Protect against unauthorised access to another user's project/media; leaked API keys; malicious or malformed uploads; path traversal; oversized uploads and resource exhaustion; abuse of transcription/render APIs; XSS, CSRF and injection; public exports or permanent media links; dependency compromise; accidental secret commits; and data loss.

## 2. Authentication and authorisation
- Use maintained authentication and secure session handling.
- Enforce backend authorisation for every project, asset, transcript, render and export operation.
- Never trust a browser-supplied project/user ID without checking ownership.
- Apply row-level security where supported and test with multiple accounts.
- Use least privilege for service credentials.
- Protect administrative operations with stronger controls, including MFA where available.
- Rate-limit authentication and expensive endpoints.

## 3. Upload and media processing
- Validate extension, declared MIME type and file signature/content.
- Generate random storage object names; never use user filenames as storage paths.
- Enforce upload size, duration, codec and processing limits.
- Store uploads privately.
- Scan or sandbox untrusted media as appropriate.
- Process media in isolated, resource-limited workers.
- Prevent path traversal, unsafe command construction and arbitrary filesystem access.
- Set timeouts and CPU/memory/disk limits.
- Clean up incomplete uploads and temporary files safely.

## 4. Secrets and providers
- Keep transcription, storage and service-role secrets server-side.
- Never commit real .env files or secrets; commit placeholders only.
- Restrict provider keys, quotas and permissions where possible.
- Rotate exposed credentials and use secret scanning.
- Disclose external media processing and obtain appropriate permission/legal basis.
- Do not enable paid APIs/infrastructure without owner approval.

## 5. Database and storage
- Use parameterised queries or safe data-access APIs.
- Enforce per-user ownership on every record and object.
- Use private storage buckets/containers.
- Issue short-lived signed links only after authorisation.
- Avoid public buckets for customer uploads/exports.
- Define retention and deletion for originals, extracted audio, transcripts, temporary renders and exports.
- Back up important metadata and test restoration.
- Protect migrations and production data.

## 6. Web application protections
Evaluate and implement protections appropriate to the stack: HTTPS, secure cookie/session configuration, Content Security Policy, XSS output encoding, CSRF protection where applicable, schema validation, safe URL handling, dependency scanning, secure CORS and no secrets/sensitive customer data in client bundles or logs.

## 7. Privacy
Explain what media/transcript data is collected, which providers process it, where it is stored, retention periods, deletion options, model-training policy and incident contact. Default: do not use customer media for model training without explicit permission and an appropriate legal basis. Review applicable Indian privacy/data-protection requirements with qualified counsel before launch; this plan is not legal advice.

## 8. Security testing
Test cross-user project/media access, signed-link authorisation and expiry, malformed/oversized uploads, rate limits, XSS/CSRF/injection, dependency vulnerabilities, secret leakage, deletion and backup restoration. Fix critical/high-severity issues before public launch. Arrange independent security assessment before significant customer volumes.

## 9. Incident response
Document steps to disable compromised keys/providers, revoke sessions and signed links, isolate processing workers, investigate affected projects, restore backups and communicate incidents under applicable obligations.

Never claim the platform is unhackable or fully secure merely because controls are listed.
