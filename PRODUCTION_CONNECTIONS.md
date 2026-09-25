# IETA Legal — Production Connections Runbook

**Purpose:** Complete the external services, infrastructure, security, and human approvals required to move IETA Legal from a validated pre-production foundation to an approved production service.

**Current state:** The Django application, local workflows, safety boundaries, tests, and deployment foundation are implemented. Several official adapters are deliberately placeholders and will not become production-ready by adding environment variables alone.

## 1. Completion order

Complete the work in this order:

1. Product, legal, privacy, and identity contracts.
2. Production cloud account, network, DNS, TLS, secrets, and deployment environment.
3. Managed database and distributed cache.
4. Global IETA identity integration.
5. Private object storage and document scanning.
6. AURA provider integration and safety evaluation.
7. Email/SMS notification delivery.
8. Monitoring, audit retention, backups, restore testing, and incident response.
9. Calling/WebRTC only if that scope is approved.
10. Chainlit only as a separately approved AURA interface experiment.

Do not open the service to real users while a required contract, security review, or data-protection decision is unresolved.

## 2. Connection summary

| Connection or decision | Required for launch | Current code state | Main work remaining |
|---|---:|---|---|
| Cloud account and deployment environment | Yes | Docker/Gunicorn foundation exists | Provision and secure the runtime |
| DNS and TLS | Yes | Application supports HTTPS settings | Configure domain, certificate, redirects, and renewal |
| Secret manager | Yes | Environment variables are supported | Store, rotate, and audit production secrets |
| Managed SQL database | Yes | Django database layer exists | Provision PostgreSQL/MySQL-compatible service, migrate, backup, and tune |
| Shared cache | Yes for multi-instance production | Cache-backed rate limits exist | Provision Redis-compatible cache and configure it |
| Global IETA identity | Yes | Fail-closed adapter boundary exists | Implement the official protocol and claims mapping |
| Private object storage | Yes if documents remain in scope | Local filesystem only; cloud adapter placeholder | Implement and secure private storage |
| Document malware scanning | Yes if uploads remain in scope | Scanner boundary and manual-review fallback exist | Connect scanner, verdict mapping, and approval policy |
| AURA provider | Yes if AURA remains in scope | Mock provider and fail-closed adapter exist | Implement official API client and safety contract |
| Email/SMS provider | Required for recovery and external notices | In-app notifications only | Implement delivery, consent, retries, and audit |
| Monitoring and alerting | Yes | Health/readiness endpoints exist | Connect telemetry, dashboards, alerts, and ownership |
| Durable audit storage | Yes | Local audit records exist | Define retention and protected export/sink |
| Backups and recovery | Yes | Recovery documentation exists | Configure backups and complete restore tests |
| Calling/WebRTC | Optional | Lifecycle/mock boundary only | Add signaling, TURN, browser media, recording and safety controls |
| Chainlit | Optional | Not installed or integrated | Evaluate separately without replacing Django controls |
| Payments | Optional | Not implemented | Define scope, provider, tax/refund/fraud policy before coding |

## 3. Cloud runtime and deployment

### Required connection

Choose one approved runtime: Azure App Service/Container Apps, Kubernetes, a managed container platform, or an equivalent platform that supports HTTPS, health probes, horizontal scaling, WebSockets if calling/Chainlit are enabled, and private network access to the database/cache/storage.

### Configure

- Production container image from the repository `Dockerfile`.
- Gunicorn process and worker count appropriate for the selected runtime.
- HTTPS termination and forwarded-protocol handling.
- `/health/live/` for liveness and `/health/ready/` for readiness.
- Deployment-managed environment variables only; do not copy `.env` files into the image.
- Release steps: install image, run migrations, collect static assets, start application, run smoke tests.
- Separate development, staging, and production resources.

### Completion test

```powershell
python manage.py check --deploy --settings=config.settings.production
python manage.py migrate --plan --settings=config.settings.production
```

Then confirm the platform can reach `/health/live/` and `/health/ready/` from its health-probe network.

## 4. Domain, DNS, and TLS

### Required connection

Register the approved public domain and point DNS to the production ingress.

### Configure

- A/AAAA or CNAME record for the public application host.
- TLS certificate managed by the cloud ingress or approved certificate service.
- Automatic certificate renewal and expiry alerting.
- HTTP-to-HTTPS redirect.
- `DJANGO_ALLOWED_HOSTS` with only approved hostnames.
- `DJANGO_CSRF_TRUSTED_ORIGINS` with HTTPS origins only.
- `SECURE_SSL_REDIRECT=True`.
- Secure, HttpOnly session and CSRF cookies.
- Content Security Policy and other production headers after frontend/CDN review.

### Completion test

- Verify the certificate chain, hostname, expiry, renewal, and TLS policy.
- Verify an HTTP request redirects to HTTPS.
- Verify an unapproved Host header is rejected.
- Verify login, logout, password reset, upload, and form POSTs work only over HTTPS.

## 5. Secrets and configuration management

Use a cloud secret manager or equivalent. Do not store production values in GitHub, `.env.example`, source files, Docker layers, browser code, logs, or issue comments.

### Required secrets and settings

| Environment variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Strong production Django signing key |
| `DJANGO_ALLOWED_HOSTS` | Approved production hostnames |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Approved HTTPS origins |
| `DB_*` | Managed database connection |
| `GLOBAL_IETA_*` | Official identity connection |
| `AURA_*` | Official AURA connection |
| `PRIVATE_STORAGE_BACKEND` and provider settings | Private file storage |
| `DOCUMENT_SCANNING_*` | Malware/content scanner |
| `NOTIFICATIONS_*` | Email/SMS delivery boundary |
| `CALLING_*` | Signaling provider, if enabled |
| Cache settings | Shared cache connection and TLS settings |
| Email settings | Password reset and service email delivery |

### Required secret controls

- Separate secret values per environment.
- Least-privilege service identity for the application.
- Rotation schedule and emergency revocation procedure.
- Access audit logs.
- No secrets in application log messages or exception payloads.
- Key/certificate expiry alerts.

## 6. Managed SQL database

### Current state

The application uses Django models and migrations. SQLite is suitable only for local development. Production settings can use a non-SQLite Django database engine through `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, and `DB_CONN_MAX_AGE`.

### Required connection

Provision a managed PostgreSQL database or another approved Django-supported SQL service. PostgreSQL is the recommended production target for this application.

### Configure

- Private network access where available.
- TLS-encrypted database connection.
- Application database user with only required schema/data permissions.
- Separate migration/release identity if the platform requires it.
- Connection pooling or a suitable `DB_CONN_MAX_AGE` value.
- Automated backups, point-in-time recovery, retention, and restore testing.
- Database monitoring for connections, CPU, storage, locks, slow queries, and failures.
- Time zone and collation policy.

### Required data decisions

- User/account retention period.
- AURA conversation retention and deletion behavior.
- Document metadata retention.
- Audit-event retention and immutability expectations.
- Privacy-request state transitions after deletion/access requests.

### Completion test

```powershell
python manage.py migrate --settings=config.settings.production
python manage.py check --deploy --settings=config.settings.production
```

Run a staging restore test from backup and verify that the application can read/write a test account, matter, conversation, notification, and audit event.

## 7. Shared cache

### Current state

The application uses Django cache for rate limits and readiness checks. A local cache is not sufficient for multiple application instances.

### Required connection

Provision a managed Redis-compatible cache with TLS, private access, authentication, eviction policy, monitoring, and high-availability settings appropriate to the selected SLA.

### Configure

- Django cache backend and connection URL/settings.
- TLS and certificate validation.
- Separate cache namespace per environment.
- Capacity and eviction policy that cannot silently remove rate-limit safety state too aggressively.
- Availability alerting.

### Completion test

- Run the readiness endpoint against the production cache.
- Send repeated login/AURA/message/document/call requests and confirm limits are shared across application instances.
- Fail one application instance and confirm rate-limit behavior remains consistent.

## 8. Global IETA identity and authentication

### Current state

The repository contains a fail-closed Global IETA provider boundary, but `GlobalIetaClient.resolve_identity()` is intentionally a placeholder. Production authentication cannot be completed by setting credentials alone.

### Owner must provide

- Authoritative protocol: OAuth/OIDC, signed token exchange, API session, or another approved contract.
- Authorization/token endpoint and identity endpoint, if applicable.
- Client ID and client secret or workload identity method.
- JWKS/signing-key discovery and key rotation policy, if tokens are used.
- Redirect URIs and post-logout redirect URIs.
- Required scopes and claims.
- Stable subject identifier.
- Email, display-name, active-status, and role/entitlement claims.
- User provisioning and deprovisioning behavior.
- Session expiry, refresh, logout, and revocation behavior.
- Failure, timeout, retry, and incident behavior.

### Application work remaining

- Implement the official client transport.
- Map the official identity response into the existing `ExternalIdentity` and `IdentitySession` models.
- Map approved claims into `UserProfile` and `AdvocateProfile` without trusting user-controlled role fields.
- Implement login callback/token validation or the approved equivalent.
- Add timeout, retry, circuit-breaker, and audit behavior.
- Add contract tests using owner-provided fixtures and non-production credentials.

### Completion test

- User login and logout.
- Advocate login and logout.
- Expired token/session.
- Revoked user.
- Wrong tenant/issuer/audience.
- Missing role claim.
- Account role change.
- Provider timeout and provider outage.
- No identity secret appears in logs or responses.

## 9. AURA provider

### Current state

The native Django AURA workspace is implemented. It persists conversations, validates input and output, rate-limits requests, checks ownership, records audit events, and uses a factual-only mock when no official AURA credentials are configured. The official AURA client currently fails closed.

### Owner must provide

- Official API base URL.
- Authentication method and secret/token delivery.
- Model/deployment identifier.
- Request schema and response schema.
- Streaming or non-streaming behavior.
- Maximum input/output tokens and message length.
- Timeout, retry, idempotency, and rate-limit policy.
- Data residency and retention behavior.
- Prompt/versioning policy.
- Safety policy for legal-information boundaries.
- Provider logging and data-use policy.
- Human escalation and unsafe-output handling.

### Application work remaining

- Implement `AuraClient.execute()` against the owner-supplied contract.
- Preserve the existing `AIProvider` interface.
- Map provider failures to safe application responses.
- Validate provider output before persistence.
- Add timeout/retry/circuit-breaker behavior.
- Add contract tests with approved fixtures.
- Perform red-team tests for legal advice, predictions, recommendations, fabricated facts, personal data leakage, prompt injection, and unsafe instructions.

### Completion test

- Factual intake response.
- Empty/oversized input.
- Provider timeout.
- Invalid provider response.
- Rate-limit behavior across instances.
- Cross-user conversation access attempt.
- Deletion/privacy request behavior.
- Audit event correctness.

## 10. Private document storage

### Current state

Local private filesystem storage is available for development only. The official storage provider is a placeholder and reports not production-ready.

### Required connection

Provision private object storage such as an approved S3-compatible or Azure Blob private container.

### Configure

- Private bucket/container with public access disabled.
- Workload identity or narrowly scoped access key.
- Encryption at rest and customer-managed key policy if required.
- TLS-only transport.
- Object ownership and path strategy.
- Lifecycle/retention rules.
- Versioning and recovery policy.
- Malware scanning handoff.
- No public media URL; downloads must remain authorised and application-mediated or use short-lived signed URLs.

### Application work remaining

- Implement the provider methods behind `PrivateStorageProvider`.
- Replace local filesystem writes for production.
- Add upload, download, delete, and metadata operations.
- Add object-not-found and provider-outage handling.
- Add storage contract tests and access-control tests.

## 11. Document malware/content scanning

### Current state

The application validates file names, content types, and size, then uses a manual-review development boundary. The official scanner client is a placeholder.

### Owner must provide

- Scanner API/base URL.
- Authentication method.
- Synchronous or asynchronous scan flow.
- Accepted file types and size limits.
- Verdict schema: clean, infected, unsupported, failed, pending.
- Quarantine behavior.
- Timeout/retry policy.
- Scan-result retention and audit requirements.
- False-positive and manual override policy.

### Completion test

- Clean document.
- Malware test file supplied by the scanner vendor.
- Unsupported type.
- Oversized file.
- Scanner timeout/outage.
- Re-scan and manual review.
- Document cannot be downloaded before approval.

## 12. Email and SMS notifications

### Current state

In-app notifications are implemented. External notification delivery is only a boundary; configuring an endpoint does not currently send email or SMS.

### Required connection

Choose an approved transactional email provider and, if needed, an SMS provider.

### Configure and decide

- Verified sender domains and phone numbers.
- API credentials or workload identity.
- Email templates and SMS templates.
- Password-reset delivery.
- Consultation and message notification rules.
- User consent and opt-out behavior.
- Bounce, complaint, unsubscribe, and invalid-number handling.
- Retry and dead-letter policy.
- Provider delivery status and audit mapping.
- Message retention and sensitive-data redaction.

### Application work remaining

- Implement `NotificationDeliveryProvider` delivery methods.
- Connect password reset to a real email backend.
- Add idempotency keys and retry handling.
- Persist provider message IDs and delivery states.
- Add delivery audit events without storing unnecessary message content.

## 13. Calling and WebRTC — optional scope

### Current state

The application has participant authorization and call-lobby lifecycle records. It does not transmit audio/video.

### Required connections if calling is approved

- Signaling service.
- STUN/TURN service.
- Browser WebRTC client and permission handling.
- Reconnect and session expiry behavior.
- Call participant authorization.
- Recording provider only if explicitly approved.
- Recording consent, retention, deletion, and legal policy.
- Emergency/safety escalation policy.
- Provider health, cost, and abuse monitoring.

The current `CALLING_API_BASE_URL` and `CALLING_API_KEY` settings are not enough; the official signaling client and browser media workflow must be implemented and reviewed.

## 14. Monitoring, logging, audit, and operations

### Required connections

- Application performance monitoring.
- Centralized structured logs.
- Error tracking with sensitive-data filtering.
- Metrics and dashboards.
- Uptime checks for public and private health endpoints.
- Alert routing and on-call ownership.
- Durable audit sink with retention and access controls.
- Deployment and migration telemetry.

### Minimum alerts

- Application health/readiness failure.
- Database connection failure or storage exhaustion.
- Cache unavailable.
- Authentication provider errors or elevated login failures.
- AURA provider errors, unsafe-output events, or rate-limit spikes.
- Document scanner/storage outage.
- Notification delivery failures.
- High error rate, latency, CPU, memory, and worker exhaustion.
- Backup failure and certificate/secret expiry.

## 15. CI/CD and release management

### Current state

GitHub Actions runs checks, production settings validation, migration drift detection, tests, and compilation.

### Required connections

- GitHub repository branch protection for `master`.
- Required CI checks before merge.
- Container registry.
- Deployment identity using OIDC/workload identity rather than long-lived keys where supported.
- Staging environment and approval gate.
- Production environment with protected secrets.
- Migration release step.
- Static collection step.
- Rollback strategy for application and migrations.
- Deployment audit trail.

## 16. Human approvals still required

These are not software connections and cannot be solved by configuration:

- Legal wording, representation boundaries, terms, disclaimer, and privacy policy.
- Consent purposes, retention, access, deletion, and data residency.
- Advocate verification and operational ownership.
- Conflict-of-interest handling and escalation.
- AURA safety evaluation and prohibited-output policy.
- Threat model, abuse cases, identity assurance, and incident response.
- Accessibility and responsive visual review.
- Document scanning and manual approval policy.
- Calling/recording policy if calling is enabled.
- Backup restoration and disaster-recovery sign-off.

## 17. Environment variable checklist

The exact names already supported by this repository are:

```text
DJANGO_SECRET_KEY
DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS
AUTH_PROVIDER
DEMO_MODE
AURA_ENABLED
AI_PROVIDER
AURA_API_BASE_URL
AURA_API_KEY
AURA_MODEL
GLOBAL_IETA_API_BASE_URL
GLOBAL_IETA_CLIENT_ID
GLOBAL_IETA_CLIENT_SECRET
DB_ENGINE
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DB_CONN_MAX_AGE
PRIVATE_STORAGE_BACKEND
DOCUMENT_SCANNING_API_BASE_URL
DOCUMENT_SCANNING_API_KEY
NOTIFICATIONS_API_BASE_URL
NOTIFICATIONS_API_KEY
CALLING_API_BASE_URL
CALLING_API_KEY
RATE_LIMIT_WINDOW_SECONDS
RATE_LIMIT_LOGIN
RATE_LIMIT_AURA
RATE_LIMIT_MESSAGES
RATE_LIMIT_DOCUMENTS
RATE_LIMIT_CALLS
```

Some provider-specific values will need to be added after the owner supplies the official contracts. Do not invent variable names or provider behavior before that contract exists.

## 18. Final release gate

Release only when all of the following are true:

- Production settings pass `python manage.py check --deploy --settings=config.settings.production`.
- Migrations apply successfully to the managed database.
- Database backup and restore have been tested.
- Shared cache is connected and tested across more than one application instance.
- Global IETA login/logout/role mapping is contract-tested.
- AURA provider is contract-tested and safety-reviewed.
- Private storage and malware scanning are active.
- Password reset and approved notification flows deliver successfully.
- Health checks, monitoring, alerting, audit retention, and on-call ownership are active.
- DNS, TLS, security headers, secrets, and certificate rotation are verified.
- Privacy, legal, security, accessibility, and operations reviews are signed off.
- Staging smoke tests pass before the production deployment.

Until these gates are complete, the correct project classification is **validated pre-production foundation**, not production-ready.
