# Security Notes (MVP -> Production Path)

## Current MVP Controls
- Input validation via Pydantic schemas.
- Emergency escalation and human verification flags.
- No direct exposure of database internals in API responses.
- Minimal CORS policy currently permissive for development only.

## Required Security Upgrades
1. Secure Login
- Implement user accounts with hashed passwords (`bcrypt`).
- Introduce JWT access tokens and short expiration.
- Add role model (admin/clinician/operator).

2. API Protection
- Enforce authentication on all non-health endpoints.
- Add rate limiting to prevent abuse.
- Add request size limits and stricter validation.

3. Data Protection
- Encrypt sensitive fields at rest where possible.
- Never log plaintext credentials or sensitive identifiers.
- Use environment variables/secrets manager for keys.

4. Transport Security
- Enforce HTTPS in deployment (reverse proxy + TLS).
- Enable HSTS in production.

5. Operational Safety
- Audit logs for access and changes.
- Alerting for suspicious access patterns.
- Backup and recovery procedures tested regularly.

## Disclaimer Handling
- Every clinical output must include medical disclaimer text.
- UI should clearly show: "AI support tool, not final diagnosis."
