# Security baseline

Django CSRF middleware, escaped template output, secure session defaults, clickjacking protection, production secure-cookie settings, environment-only secrets, password validators, login rate limiting, and role-gated views are enabled. Matter access has an explicit `MatterAccess` grant model and the service layer checks ownership or grants.

Demo mode is a local exploration mechanism, not authentication. Production settings set `DEMO_MODE=False` and require a real secret and allowed hosts. Private documents must use a private storage adapter when implemented; the current `static/` directory is never a document store.

Remaining production work includes formal audit event coverage, upload content validation, external identity verification, secure private-media delivery, CSP policy tuning, and a complete threat-model review with the owner and security reviewers.

The development document flow now rejects executable extensions, caps files at 10 MB, stores randomised names outside public static assets, downloads as attachments, and checks matter ownership or advocate relationship before access. MIME metadata remains untrusted and files stay pending review until production scanning is supplied.

Rate limiting is exposed through `apps.core.rate_limit` and configured through environment-backed settings for AURA, messages, documents, and calls. Audit events currently cover AURA messages, document uploads, consultation decisions, and secure messages. A shared production cache and durable audit sink should replace the local development implementations before multi-process deployment.

Sensitive throttled responses expose only `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After`. Rate-limit events are audited by action and bucket without storing request bodies.

Private files remain unavailable while `PENDING_REVIEW`. Only the admin-role review route can approve or reject them, and review actions are audited. Development uploads are not automatically scanned; a configured but unimplemented scanner blocks storage and approval.

Privacy controls are user-scoped and versioned. Deletion requests are recorded rather than executed automatically, preventing accidental destructive changes before a reviewed retention policy and identity verification flow exist.

Privacy request transitions are monotonic and terminal states cannot be reopened through the admin route. Queue age is informational only and does not create an automatic deletion deadline.

Request IDs are accepted only when bounded to safe characters and length, otherwise a new identifier is generated. Readiness checks do not expose credentials or database details.

Audit events persist the bounded request ID when an action occurs inside an HTTP request. This supports support-ticket correlation without copying request bodies or secrets into the audit record.

The admin audit view caps historical results and paginates them, limiting the amount of operational data returned in one response.

Call lobbies require a confirmed consultation and a user/advocate relationship. The development simulation explicitly reports that no audio or video is transmitted.

AURA conversation IDs are checked against the current user before reads or writes. The persisted model stores the bounded interaction and response, while the AURA safety boundary remains server-controlled.

AURA user messages and provider responses are bounded and validated before persistence. Official provider failures and invalid responses fail closed without exposing provider details to the user.

Production authentication defaults to the fail-closed Global IETA provider. Local username/password authentication is selected only by development configuration, and no default passwords are committed.

Matter detail access is filtered by ownership for users and selected-advocate relationship for advocates before the object is fetched.

Intake review, editing, and confirmation are restricted to the owning user. Confirmation changes workflow state only and does not grant advocate access by itself.

Profile updates are limited to the current development session identity and, for advocates, their legal-domain profile. No duplicate production authentication or password storage is introduced.

Privacy request operations require the simulated `ADMIN` role and are recorded in the audit log. The implementation intentionally stops at status tracking until verified identity, retention, and deletion procedures are approved.

Notification records are recipient-scoped and represent in-app availability only. External email/SMS delivery remains unavailable until its provider contract, consent rules, retry behavior, and audit policy are supplied.

Notification read actions are audited as `notification.read` or `notifications.read_all`; bulk events record only the affected count and never copy notification bodies into the audit log.
