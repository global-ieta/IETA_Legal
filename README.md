# IETA Legal

IETA Legal is a modular Django application for organising user-provided facts and connecting users with independently verified advocates. It is a connected product within the Global IETA ecosystem; it is not an AI lawyer, law firm, legal marketplace, or substitute for professional advice.

## Current status

The product foundation is implemented and validated. The application now includes professional account authentication, role-resolved portals, factual intake, advocate workflows, secure messaging, private documents, privacy requests, and clear customer-facing product boundaries.

The project is a validated pre-production foundation. It must not be described as production-ready until the official identity, AI, storage, scanning, delivery, database, calling, operations, and human-review requirements are completed.

See [Project_Status.md](Project_Status.md) for the detailed current-state report.
See [Project_Report.md](Project_Report.md) for the full project progression and Chainlit/AURA assessment.

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and use **Sign in** or **Create an account**. Local development uses `AUTH_PROVIDER=development`; production defaults to the fail-closed `global_ieta` provider until the official Global IETA contract is configured.

No default password is shipped. Create an account through **Get started**, then sign in with the credentials you created. The local sample records created by `seed_demo_workspace` are workflow data and do not have documented login passwords.

For a repeatable local workflow dataset, run:

```powershell
python manage.py seed_demo_workspace
```

The command is intended only for local development and is disabled when demo mode is off.

## Configuration

Configuration is supplied through environment variables. Use [.env.example](.env.example) as a safe placeholder reference; it contains no real credentials.

Important production settings include:

- `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and `DJANGO_CSRF_TRUSTED_ORIGINS`
- `AUTH_PROVIDER=global_ieta`
- Managed database settings
- Private storage and document-scanning settings
- Shared cache, notification, AURA, and calling integration settings

Production settings reject weak secrets, wildcard hosts, unsafe origins, unsupported local storage, and unintended SQLite usage.

## Implemented capabilities

- Public site pages, navigation, SEO metadata, sitemap, robots policy, and custom error pages.
- Professional split sign-in with dedicated User Workspace and Advocate Workspace panels, username/email lookup, password visibility control, forgot-password flow, account registration, advocate registration, logout, hashed passwords, and session-backed authentication.
- Replaceable authentication-provider boundary for future Global IETA identity integration.
- Automatic account-role resolution for user, advocate, and admin workspaces with workspace-aware sign-in validation.
- Factual intake with draft, edit, review, and confirmation workflow.
- Matter workspaces with scoped facts, timelines, questions, documents, consultations, conversations, and advocate context.
- Advocate directory, profile display, consultation requests, conflict-check state, and accept/decline workflow.
- Recipient-scoped secure messaging and in-app notifications.
- Persisted AURA factual-intake conversations with a non-advisory provider boundary.
- Private matter documents with allowlists, size limits, randomised storage names, object-level access, pending review, and audited downloads.
- Participant-scoped call-lobby workflow with no media transmission until the official calling contract is connected.
- Privacy Centre with versioned consent, access/deletion requests, and terminal workflow states.
- Admin document review, privacy operations, integration status, audit filtering, request-ID tracing, and pagination.
- Health endpoints for liveness, database/cache readiness, and integration configuration state.
- Cache-backed rate limits with safe response headers and minimal audit events.
- Responsive customer-facing UI with branded SVG landing artwork, scroll and hover animation, accessible focus states, reduced-motion support, loading states, clear empty states, and professional authentication screens.

## Integration boundaries

External dependencies are environment-driven and isolated behind replaceable interfaces. No credentials or undocumented network contracts are committed.

Current boundaries include:

- Global IETA identity and authentication.
- AURA provider and factual-intake contract.
- Calling, signaling, and TURN infrastructure.
- Private document storage.
- Document malware/content scanning.
- Email/SMS notification delivery.

Development fallbacks are explicit and fail closed when an official provider is selected but not implemented.

## Validation

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py test --settings=config.settings.testing
python -m compileall -q .
```

Latest local validation: **93 tests passed**, no migration drift, no Django system-check errors, successful Python compilation, and successful static asset collection.

CI is defined in [.github/workflows/ci.yml](.github/workflows/ci.yml) and documented in [docs/CI.md](docs/CI.md).

## Deployment readiness

The included [Dockerfile](Dockerfile) runs Gunicorn as a non-root user and collects static assets without embedding application secrets. Deployment remains responsible for secret injection, migrations, external database provisioning, private storage, scanning, shared cache, TLS, backups, monitoring, and integration contracts.

Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) before deployment. Production settings reject unsafe defaults and require explicit overrides for development-only SQLite or local private storage.

## Documentation

- [Project status](Project_Status.md)
- [Project report](Project_Report.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Integration boundaries](docs/INTEGRATIONS.md)
- [Security baseline](docs/SECURITY.md)
- [Testing](docs/TESTING.md)
- [Deployment](docs/DEPLOYMENT.md)
- [CI](docs/CI.md)
- [Rebuild plan](docs/REBUILD_PLAN.md)
- [Final completion audit](docs/FINAL_COMPLETION_AUDIT.md)
- [Disaster recovery](docs/DISASTER_RECOVERY.md)
- [Production checklist](docs/PRODUCTION_CHECKLIST.md)

## Production status

- **Implemented:** Application workflows, local authentication, authorization boundaries, UI foundation, tests, CI checks, and fail-closed integration adapters.
- **Ready for production configuration:** Secure settings, database variables, migration release process, static collection, and container startup.
- **Blocked — official contract required:** Global IETA, AURA, document scanning, notifications, and calling/signaling.
- **Blocked — infrastructure required:** Managed database, private storage, shared cache, durable audit, monitoring, alerting, backups, recovery, and WebRTC/TURN.
- **Requires human review:** Legal, privacy, security, accessibility, advocate operations, threat model, and production calling/recording procedures.

Production launch requires all blocked dependencies and human reviews to be resolved.
