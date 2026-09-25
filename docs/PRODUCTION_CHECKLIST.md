# IETA Legal — Production Checklist

## Classification key

- **IMPLEMENTED**
- **READY FOR PRODUCTION CONFIGURATION**
- **BLOCKED — OFFICIAL CONTRACT REQUIRED**
- **BLOCKED — INFRASTRUCTURE REQUIRED**
- **REQUIRES HUMAN LEGAL REVIEW**
- **REQUIRES HUMAN SECURITY REVIEW**
- **REQUIRES HUMAN OPERATIONS REVIEW**

## Application

| Area | Status | Evidence or next action |
|---|---|---|
| Django modular architecture | IMPLEMENTED | `apps/` and `integrations/` boundaries are present. |
| Authentication abstraction | IMPLEMENTED | Local provider and fail-closed Global IETA provider. |
| Role-resolved portals | IMPLEMENTED | Authenticated profile role determines portal. |
| Password handling | IMPLEMENTED | Django hashing and password validators. |
| Production identity | BLOCKED — OFFICIAL CONTRACT REQUIRED | Supply Global IETA identity contract and claims. |
| Database configuration | READY FOR PRODUCTION CONFIGURATION | Supply managed database environment and run migrations. |
| Private storage | BLOCKED — INFRASTRUCTURE REQUIRED | Provision approved private object storage and configure adapter. |
| Document scanning | BLOCKED — OFFICIAL CONTRACT REQUIRED | Supply scanner contract and approval policy. |
| AURA | BLOCKED — OFFICIAL CONTRACT REQUIRED | Supply official transport, model, auth, schema, and safety contract. |
| Calling | BLOCKED — OFFICIAL CONTRACT REQUIRED | Supply signaling/TURN/WebRTC contract and infrastructure. |
| Notifications | BLOCKED — OFFICIAL CONTRACT REQUIRED | Supply email/SMS delivery contract and consent policy. |
| Shared cache | BLOCKED — INFRASTRUCTURE REQUIRED | Provision distributed cache. |
| Durable audit | BLOCKED — INFRASTRUCTURE REQUIRED | Provision protected audit sink and retention. |
| Monitoring and alerting | BLOCKED — INFRASTRUCTURE REQUIRED | Configure telemetry, alert rules, and ownership. |
| Backups and recovery | BLOCKED — INFRASTRUCTURE REQUIRED | Provision backups and complete a restore test. |

## Human review

| Area | Status |
|---|---|
| Legal wording and representation boundaries | REQUIRES HUMAN LEGAL REVIEW |
| Privacy, consent, retention, and deletion policy | REQUIRES HUMAN LEGAL REVIEW |
| Advocate verification and conflict workflow | REQUIRES HUMAN OPERATIONS REVIEW |
| Threat model and production security posture | REQUIRES HUMAN SECURITY REVIEW |
| Accessibility and responsive visual QA | REQUIRES HUMAN REVIEW |
| Calling, recording, and safety procedures | REQUIRES HUMAN LEGAL REVIEW |

## Release validation

Run with deployment-provided values:

```powershell
python manage.py check --deploy --settings=config.settings.production
python manage.py migrate --plan --settings=config.settings.production
python manage.py makemigrations --check
python manage.py test --settings=config.settings.testing
python -m compileall -q .
```

Do not release while any required blocked dependency or human review remains unresolved.
