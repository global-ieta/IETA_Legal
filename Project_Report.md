# IETA Legal — Project Report

**Report date:** 25 September 2026  
**Current classification:** Validated pre-production foundation  
**Latest validation:** 93 tests passed; Django checks, migration check, compilation, and static collection passed

## 1. Purpose

IETA Legal is a modular Django application for helping users organise factual information, prepare for a professional conversation, and choose how they connect with an independent advocate.

The platform is not an AI lawyer, law firm, legal marketplace, or substitute for professional advice. AURA is deliberately limited to factual information gathering and organisation. Advocates remain independent professionals.

This report explains how the project progressed from its initial foundation to the current implementation, what is working now, what remains external or incomplete, and how Chainlit could fit into the future AURA interface.

## 2. Repository history note

The repository does not contain a usable Git commit history. The sequence below is reconstructed from the rebuild plan, implementation boundaries, current source, tests, completion documents, and the latest UI updates. It describes the implementation progression, not an audited commit-by-commit history.

## 3. Development progression

### Phase 1 — Foundation and public site

- Established the Django project structure and environment-based settings.
- Added modular application boundaries under `apps/`.
- Added replaceable external integration boundaries under `integrations/`.
- Created the public information site, navigation, SEO metadata, robots policy, sitemap, and custom error pages.
- Introduced the IETA Legal visual system: dark surfaces, gold accents, editorial typography, responsive layout tokens, and accessible focus states.

### Phase 2 — Development roles and portals

- Added development-only workflow identities and an idempotent `seed_demo_workspace` command.
- Added separate user, advocate, and admin portal contexts.
- Added role-aware routing and permission checks.
- Kept development sessions separate from production authentication.

### Phase 3 — Core legal-information workflow

- Added factual intake creation, editing, review, and confirmation.
- Added matter records with user ownership and authorised relationship scoping.
- Added advocate directory and profile display.
- Added consultation requests, pending conflict checks, advocate accept/decline decisions, and status transitions.
- Added relationship-scoped messaging and notifications.

### Phase 4 — Privacy, documents, calling, and operations

- Added versioned consent preferences and privacy access/deletion request tracking.
- Added private documents with extension/content-type validation, size limits, private storage paths, review status, and object-level access checks.
- Added admin document review, privacy queues, audit views, and integration-status visibility.
- Added participant-scoped calling lifecycle and call-lobby states without claiming browser media, WebRTC, TURN, or recording support.
- Added liveness, database/cache readiness, and integration-status endpoints.

### Phase 5 — AURA safety boundary

- Added the `AIProvider` interface and an explicit AURA provider selector.
- Added the factual-only development mock provider.
- Added the official AURA adapter and client boundary, which fail closed until the owner supplies the official contract.
- Added persisted `AuraConversation` and `AuraMessage` records.
- Added conversation ownership checks so users cannot access another user’s AURA conversation.
- Added input length validation, provider-response validation, rate limiting, and audit events.
- Added a server-controlled safety prompt that prohibits legal advice, legal opinions, recommendations, rankings, predictions, invented facts, and deadline calculations.

### Phase 6 — Production-oriented completion pass

- Removed committed build secrets and strengthened production configuration handling.
- Added explicit production authentication selection with a fail-closed Global IETA provider.
- Retained local username/password authentication only for development configuration.
- Added password validation, login rate limiting, safe unavailable responses, and security-oriented configuration checks.
- Added final audit, production checklist, disaster recovery, integration, security, deployment, testing, and project-status documentation.

### Phase 7 — Authentication and portal UX refinement

- Replaced the single login presentation with separate User Workspace and Advocate Workspace panels.
- Added workspace-aware login validation so credentials must use the matching panel.
- Added shared sticky navigation for user, advocate, and admin portal pages.
- Added responsive mobile navigation behavior.
- Added safe display-name fallbacks for authenticated and legacy local sessions.

### Phase 8 — Latest landing-page refinement

- Added a branded IETA Legal SVG hero composition.
- Added a reusable IETA Legal mark SVG for the hero metadata and feature cards.
- Added animated SVG orbit, ring, and signal details.
- Added landing-page scroll reveal transitions using `IntersectionObserver`.
- Added pointer-responsive hero depth on suitable pointer devices.
- Added feature-card hover movement and surface transitions.
- Preserved reduced-motion behavior for users who request it.
- Collected all new assets into `staticfiles/`.

## 4. Current architecture

| Area | Current implementation | Current state |
|---|---|---|
| Web framework | Django with server-rendered templates | Implemented |
| Authentication | Local provider for development; fail-closed Global IETA boundary for production | Contract pending for production |
| Roles | User, advocate, and admin profiles with role-aware portal access | Implemented foundation |
| AURA UI | Native Django workspace at `/aura/` with persisted conversation history | Implemented with development mock |
| AURA provider | `AIProvider`, mock provider, official adapter, client, validators | Official contract pending |
| Data | SQLite development configuration and Django models | Managed production database pending |
| Private documents | Local private storage boundary and manual review state | Production storage/scanning pending |
| Notifications | Recipient-scoped in-app records | External delivery pending |
| Calling | Authorised call-lobby lifecycle | WebRTC/TURN/signaling pending |
| Frontend | Responsive HTML/CSS/JavaScript with SVG visual assets | Implemented foundation |
| Deployment | Docker/Gunicorn/static collection/health checks/CI | Configuration and infrastructure pending |

## 5. Current AURA implementation

The current AURA flow is intentionally part of the Django application:

1. An authenticated user opens the AURA workspace.
2. The server resolves the user’s active conversation.
3. The browser submits a factual message to `/aura/message/`.
4. The server validates the user, role, request size, rate limit, and conversation ownership.
5. The selected AURA provider returns a response.
6. The response is validated before persistence.
7. The user message, assistant message, and audit event are stored.
8. The browser receives the bounded response as JSON and updates the conversation view.

This arrangement keeps identity, permissions, conversation ownership, rate limits, audit events, safety boundaries, and persistence inside the IETA Legal application.

## 6. Chainlit assessment for AURA

### What Chainlit is

Chainlit is a Python framework for conversational AI interfaces. Its official documentation describes support for authentication callbacks, streaming messages and steps, data persistence through data-layer options, and multiple consumption modes including a native web app, Copilot embedding, and custom React frontends.

References:

- [Chainlit overview](https://docs.chainlit.io/data-persistence/custom)
- [Authentication overview](https://docs.chainlit.io/authentication/overview)
- [Streaming](https://docs.chainlit.io/advanced-features/streaming)
- [Data persistence](https://docs.chainlit.io/data-persistence/overview)
- [Deployment and WebSocket requirements](https://docs.chainlit.io/deploy/overview)

### What Chainlit could improve

- A faster conversational UI prototype for AURA.
- Token-by-token response streaming.
- Visible step/activity presentation for multi-stage factual gathering.
- A dedicated AI experimentation surface for approved internal testing.
- A possible embedded assistant experience through a supported embedding or custom frontend approach.

### What Chainlit would not replace

Chainlit would not replace the IETA Legal domain layer. The following must remain controlled by Django and the IETA Legal integration boundary:

- Global IETA identity and role resolution.
- User and conversation ownership checks.
- Consent, privacy, retention, and audit policy.
- AURA safety rules and response validation.
- Rate limiting and abuse controls.
- The official model/API contract.
- Canonical persistence of user and assistant messages.

### Important integration considerations

- Chainlit applications are public by default until authentication is configured. Its authentication must be connected to the existing IETA identity model rather than creating a second unrelated account system.
- Chainlit data persistence is not automatic. A production implementation would need an approved data layer or a controlled adapter that preserves IETA Legal as the canonical conversation store.
- Chainlit uses WebSockets. The deployment platform, reverse proxy, scaling strategy, sticky-session behavior, and observability must support that transport.
- A separately hosted Chainlit UI would require explicit origin, CSRF/session, authorization, and token-handling decisions.
- AURA must not expose hidden reasoning, private provider data, or unsafe intermediate content merely because a UI can display steps.

### Recommendation

**Do not add Chainlit to the production application yet.** The current native Django AURA interface is already connected to the correct authentication, ownership, rate-limit, audit, validation, and persistence boundaries.

If Chainlit is desired, use it first as an isolated prototype:

1. Add Chainlit in a separate experimental service or development-only app.
2. Reuse the existing AURA provider interface and validation rules.
3. Use synthetic/local data only during evaluation.
4. Measure streaming quality, factual-boundary adherence, accessibility, mobile behavior, and session isolation.
5. Decide whether Chainlit should remain an internal prototype, serve as a separate AI workspace, or be replaced by a custom frontend that calls the existing Django AURA endpoint.
6. Require an approved identity, data-layer, WebSocket, privacy, security, and operations design before production integration.

**Current Chainlit status:** Not installed, not connected, and not represented as a live dependency. It is a future interface option under evaluation.

## 7. Security and production position

Implemented controls include password hashing, password validation, session authentication, role-aware access, CSRF protection, secure production cookie settings, login/AURA/message/document/call rate limits, private document boundaries, response validation, audit events, request identifiers, and fail-closed official adapters.

The project is not production-ready until the following are supplied and reviewed:

- Official Global IETA identity contract and claims.
- Official AURA transport, model, authentication, schema, timeout, retry, and safety contract.
- Managed production database.
- Approved private object storage and malware/content scanning.
- Email/SMS delivery with consent, retry, retention, and audit rules.
- WebRTC, TURN, signaling, reconnect, recording, and safety design if calling remains in scope.
- Shared cache, durable audit storage, monitoring, alerting, backups, and recovery testing.
- Legal, privacy, security, accessibility, advocate-operations, and threat-model reviews.

## 8. Latest validation

The latest local validation completed successfully:

```text
93 tests passed
python manage.py check
python manage.py makemigrations --check --dry-run
python -m compileall -q .
python manage.py collectstatic --noinput
```

Expected test logs for intentional 404, 429, and 503 cases do not indicate failures.

## 9. Useful project documents

- [README](README.md)
- [Project status](Project_Status.md)
- [Production connections](PRODUCTION_CONNECTIONS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Integration boundaries](docs/INTEGRATIONS.md)
- [Security baseline](docs/SECURITY.md)
- [Testing](docs/TESTING.md)
- [Deployment](docs/DEPLOYMENT.md)
- [CI](docs/CI.md)
- [Final completion audit](docs/FINAL_COMPLETION_AUDIT.md)
- [Final completion report](docs/FINAL_COMPLETION_REPORT.md)
- [Disaster recovery](docs/DISASTER_RECOVERY.md)
- [Production checklist](docs/PRODUCTION_CHECKLIST.md)
