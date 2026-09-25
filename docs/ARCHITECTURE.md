# Architecture notes

IETA Legal is a Django monolith with modular Django applications and server-rendered HTML. Tailwind utilities are loaded for the current build and brand tokens are centralised in `static/css/tokens.css`. GSAP is used only for short entrance transitions and is bypassed when reduced motion is requested.

The development role mechanism stores a simulated role and a local development user ID in the Django session. `DEMO_MODE=False` removes the entry flow. Production identity is intentionally an interface in `integrations/global_ieta`; no API contract is invented.

The AURA boundary is `integrations.aura.interface.AIProvider`. `MockAuraProvider` is the active development implementation. It is factual and non-advisory by design. `OfficialAuraProvider` is scaffolded but cannot execute until the owner supplies its contract.

The official AURA adapter boundary is now scaffolded without making network calls or assuming request/response fields. Development configuration continues to use the mock provider when official credentials are absent.

The future identity path follows `external identity → IETA Legal session → legal-domain data`. The current demo session remains separate and is not a duplicate production password system. If an official AURA configuration is present before its contract is implemented, the user receives a controlled `503` response and an audit event.

Matter, consultation, and conversation views scope queries by the current role and relationship. `MatterAccess` exists for explicit grants. Private uploads must use a private storage adapter when documents are introduced; they must never be served from `static/`.

The current development journey is end-to-end: a factual intake creates a user-owned matter; the user can inspect the explicitly labelled development advocate profile; selecting a matter creates a requested consultation and a `ConflictCheck` in `PENDING` state. No conflict result or advocate acceptance is fabricated. The official advocate workflow should replace this pending state with the owner-supplied review contract.

When the related advocate accepts a request, the development workflow marks the conflict check as reviewed, confirms the consultation, creates a `Conversation`, and emits a recipient-scoped `Notification`. Declining cancels the request and returns the matter to open status. Conversation reads and writes are filtered by the user/advocate relationship at query time.

The admin portal reports counts from the development database and lists pending conflict checks without pretending to resolve them. Notification read state is recipient-scoped; individual and bulk read actions cannot affect another user's notifications.

Private documents use `apps.documents` with randomised matter-scoped storage names, an allowlist and size limit, no public media URL, and object-level access checks. New files remain `PENDING_REVIEW`; production antivirus/content inspection and private cloud storage must be connected before launch.

Document uploads pass through `integrations.documents.DocumentSafetyProvider`. The development provider records a manual-review-required marker without inspecting content. If official scanner configuration is supplied before its contract is implemented, storage and admin approval fail closed rather than creating a false safety verdict.

The document `FileField` currently uses a local private filesystem adapter with no public URL. `integrations.storage.PrivateStorageProvider` reports this as development-only; selecting a non-local backend before its implementation blocks uploads, and production validation requires a private backend unless explicitly overridden for a controlled build or test.

Rate limits are checked at the application boundary before sensitive writes. `apps.audit.services.record_event` records minimal actor/action/object metadata without storing message or document contents.

Rate-limit checks return bounded metadata for response headers and record throttled actions separately. This keeps client retry behavior visible without coupling the limit implementation to a particular cache vendor.

Pending documents cannot be downloaded. The admin review surface is a manual development control that changes a document to `AVAILABLE` or `REJECTED` and records the decision. Development approval is explicitly manual; production approval must be backed by the document-safety adapter, malware/content inspection, and an owner-supplied review policy.

The privacy centre stores versioned consent per user and purpose, plus non-destructive access/deletion requests. Requests remain `REQUESTED` until the owner supplies a verified review, retention, export, and deletion process.

The admin privacy queue exposes request age for prioritisation and permits only explicit forward transitions. `COMPLETED` and `DECLINED` requests are terminal; no transition performs data deletion.

Its controls mirror those transitions: requested items can be reviewed or declined, under-review items can be completed or declined, and terminal items have no action controls.

The public site exposes a sitemap and robots policy generated by Django. Canonical URLs and index directives are added centrally; private portal and operational paths are marked `noindex, nofollow` and are not included in the sitemap.

Operational endpoints include `/health/` for liveness, `/health/ready/` for database/cache readiness, and `/health/integrations/` for a non-secret local configuration report. The integration report never makes network calls and distinguishes development mocks from configured-but-contract-pending adapters. Every response receives a bounded `X-Request-ID` for support correlation. Django logging is configured centrally and remains deployment-configurable.

`apps.audit.services.record_event` stores that bounded request ID on each HTTP-originated event, allowing the admin audit view to correlate a workflow action with server logs while retaining minimal event metadata.

Confirmed consultations have a participant-scoped call lobby for audio/video development simulation. `CallSession` records lifecycle state and the future signaling provider name, but no media is transmitted. Production WebRTC, TURN, signaling, recording, and safety workflows remain external integration work.

The calling lobby invokes `integrations.calling.SignalingProvider` at session start and close. Development stores a generated provider session ID for traceability, while the mock provider explicitly reports that no media was transmitted. Complete calling configuration selects the official adapter, which currently fails closed rather than making an undocumented network request.

`/calls/status/` returns only active sessions belonging to the current participant. It exposes a non-secret provider state (`development-simulation` or `official-configured`) and never treats configuration presence as production readiness.

The admin portal mirrors the non-secret integration report at `/admin-portal/integrations/` for operational review. It uses the same local readiness service and remains separate from the database/cache readiness probe.

The admin operations overview derives attention counts from the domain tables for pending documents, open privacy requests, active simulated calls, and contract-pending integrations. These are development operations signals, not production SLAs or external provider health checks.

Consultation and messaging workflows create notifications through `apps.notifications.services.create_in_app_notification`. This keeps in-app delivery available while preventing external email/SMS delivery from being implied by a database record.

Notification read and bulk-read actions are recorded with minimal audit metadata, preserving operational traceability without duplicating notification content.

Administrative queue views are intentionally query-filtered: privacy requests default to open work, audit events can be narrowed by exact action, and document review is limited to pending security review. Status changes remain explicit POST actions and are audited.

Audit operators can combine the action filter with an exact bounded request ID to isolate one HTTP trace; results remain capped at the latest 100 matching events.

Audit queries use indexes for action, request ID, and chronology, then paginate the bounded result set for predictable admin response size.

The development profile page separates `UserProfile` identity display data from `AdvocateProfile` professional data. It never manages passwords or Global IETA identity claims.

Privacy requests have an admin-only operational queue at `/admin-portal/privacy/`. Status changes are explicit and audited; completing a request does not itself delete data.

User and Advocate dashboards now expose the relevant documents, consultations, messages, notifications, privacy, profile, and calling routes through role-specific navigation. The portal templates remain intentionally different in terminology and actions.

AURA conversations are persisted as user-owned `AuraConversation` and `AuraMessage` records. Each message request must reference an active conversation owned by the current demo user; refreshes do not erase the factual intake thread.

Matter detail pages compose the authorised legal-domain view: attached factual intake, timeline, questions, selected advocate, documents, consultations, conversations, and navigation links. The detail query is scoped before object lookup, so unrelated users receive a not-found response.

Intake now has explicit draft, review, edit, and confirmation steps. Confirmation records a user action and audit event; it does not turn the platform or AURA into a legal adviser.

`seed_demo_workspace` creates only clearly labelled local sample identities and workflow records, and is blocked in production mode. It is a convenience for development exploration, not a fixture for production data.

Chainlit is not used. A native Django AURA UI is smaller, keeps the workflow server-rendered, and avoids inventing a second runtime until an official AURA integration requires it.

Authentication is resolved through `apps.accounts.authentication.AuthenticationProvider`. Development configuration selects the local password provider; production configuration defaults to the fail-closed Global IETA provider. The portal and domain layers consume account role context and do not depend on an external identity transport.
