# IETA Legal — Project Status

**Status:** Pre-production foundation complete; final audit documented

**Last verified:** 25 September 2026

## Executive summary

IETA Legal is a modular Django application with a complete local product journey from account creation and factual intake through matter creation, advocate discovery, consultation workflow, secure messaging, notifications, private documents, privacy requests, and participant-scoped calling workflow.

The customer-facing experience has been refined around real authentication, automatic role resolution, clear boundaries, accessible states, and professional portal navigation. The system is not production-ready until the external identity, service, infrastructure, and operational contracts are implemented and reviewed.

## Delivered scope

### Authentication and account access

- Username/email and password sign-in.
- Password visibility control and forgot-password routes.
- User and advocate registration flows.
- Django password hashing through `create_user` and session-backed authentication.
- Provider abstraction selected through environment configuration.
- Automatic user, advocate, and admin role resolution from account data.
- Logout and authenticated portal navigation.
- No default credentials or hardcoded passwords are shipped. Users must register through **Get started**; local sample identities are workflow data, not login credentials.
- Password-reset delivery remains local until an email provider is configured.
- Legacy development entry retained only as a compatibility boundary; it is not part of the customer-facing journey.

### Product workflow

- Public information site with SEO, sitemap, robots policy, and custom error pages.
- User factual-intake lifecycle: draft, edit, review, and confirmation.
- Matter workspace with authorised relationship scoping.
- Advocate directory and profile display.
- Consultation request, pending conflict check, accept, and decline workflow.
- Relationship-scoped conversations and messages.
- Recipient-scoped in-app notifications with read and bulk-read actions.
- Persisted AURA factual-intake conversation history.
- Participant-scoped audio/video call-lobby workflow with no media transmission.

### Privacy, security, and operations

- Versioned consent preferences.
- Access and deletion request tracking without automatic deletion.
- Monotonic privacy-request transitions with terminal states.
- Private document allowlist, 10 MB limit, randomised storage path, no public media URL, and object-level access checks.
- Manual document review boundary and private-storage boundary.
- Cache-backed rate limits for AURA, messages, documents, and calls.
- Safe rate-limit headers and audited throttling events.
- Minimal audit events with bounded request-ID correlation.
- Admin queues with filters, indexes, and pagination.
- Liveness, database/cache readiness, and integration-status endpoints.
- Production configuration checks for secrets, hosts, HTTPS CSRF origins, database, and private storage.

### UI/UX refinement

- Professional split sign-in with separate User Workspace and Advocate Workspace panels.
- Workspace-aware sign-in validation prevents credentials being used through the wrong portal panel.
- Professional registration, advocate-registration, and password-reset screens.
- Branded landing-page SVG hero artwork and reusable IETA Legal mark assets.
- Landing-page scroll reveals, hero depth interaction, SVG motion, card hover states, and reduced-motion safeguards.
- No visible development/demo language in active customer journeys.
- Automatic portal routing after authentication.
- Consistent sign-in/sign-out navigation.
- Shared sticky portal navigation for user, advocate, and admin workspaces.
- Clear loading, empty, error, and unavailable states.
- Responsive layouts, keyboard-visible focus styles, password show/hide controls, and reduced-motion support.
- Product boundaries kept visible without exposing internal provider labels.
- Shared stylesheet and responsive layout assets are restored and served from `/static/` during local development.

### Engineering foundation

- Django project with modular applications under `apps/`.
- Replaceable integration boundaries under `integrations/`.
- SQLite development configuration and production database settings.
- Docker image with Gunicorn, non-root runtime, static collection, and health check.
- GitHub Actions CI for checks, production-settings smoke validation, migration drift, tests, and compilation.
- Idempotent `seed_demo_workspace` command for local workflow data.

## Integration readiness

| Area | Current state | Required before production |
|---|---|---|
| Identity and authentication | Local provider behind an abstraction | Official Global IETA identity contract and claims |
| AURA | Factual, non-advisory provider boundary | Official API contract, model, authentication, and safety review |
| Private storage | Local private filesystem boundary | Approved private cloud storage adapter |
| Document scanning | Review-state boundary without content inspection | Malware/content scanner and approval policy |
| Notifications | In-app delivery | Email/SMS provider, consent, retry, and audit policy |
| Calling | Participant-scoped workflow without media transmission | WebRTC, TURN, signaling, recording, and safety workflows |
| Database | Development SQLite | Managed production database and migration process |
| Operations | Local audit, cache, and health boundaries | Durable audit sink, shared cache, monitoring, backups, and alerting |
| Payments | Not implemented | Only if explicitly approved and specified |

Configured but unimplemented official integrations fail closed. Credentials alone do not make an integration production-ready.

## Latest validation

The latest local validation completed successfully:

- 93 tests passed.
- `python manage.py check` passed.
- `python manage.py makemigrations --check` reported no changes.
- `python -m compileall -q .` passed.
- `python manage.py collectstatic --noinput` completed successfully.

Expected log warnings for intentional 404, 429, and 503 test cases do not indicate test failures.

## Current local access

- Start the server with `python manage.py runserver`.
- Open `http://127.0.0.1:8000/`.
- Select **Get started** to create an account, then use **Sign in**.
- The database may contain `demo_user`, `demo_advocate`, and `demo_admin` sample records, but no default password is assigned to them.

## Remaining production gates

1. Confirm and integrate the official Global IETA identity contract.
2. Confirm and integrate the official AURA service and safety contract.
3. Provision the production database, private storage, and document scanner.
4. Connect email/SMS delivery with consent, retry, retention, and audit rules.
5. Complete the production calling design, including WebRTC, TURN, signaling, recording, and safety handling.
6. Provision shared cache, durable audit storage, monitoring, backups, and alerting.
7. Complete legal, privacy, security, advocate-operations, accessibility, and threat-model review.

## Reference documents

- [README](README.md)
- [Project report](Project_Report.md)
- [Production connections](PRODUCTION_CONNECTIONS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Integration boundaries](docs/INTEGRATIONS.md)
- [Security baseline](docs/SECURITY.md)
- [Testing](docs/TESTING.md)
- [Deployment](docs/DEPLOYMENT.md)
- [CI](docs/CI.md)
- [Final completion audit](docs/FINAL_COMPLETION_AUDIT.md)
- [Disaster recovery](docs/DISASTER_RECOVERY.md)
- [Production checklist](docs/PRODUCTION_CHECKLIST.md)
