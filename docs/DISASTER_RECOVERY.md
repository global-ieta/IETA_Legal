# IETA Legal — Disaster Recovery Runbook

This runbook is configuration-dependent. It documents the recovery procedure without claiming that backups or recovery infrastructure currently exist.

## Current state

- Local development uses SQLite and local private storage.
- The repository does not provide production backup storage, a backup schedule, a restore service, or a tested recovery environment.
- Production backup ownership, retention, encryption, and recovery objectives require operations approval.

## Required production configuration

Before launch, the owner must define and provision:

- Production database backup schedule and retention.
- Private-document storage versioning, backup/replication, and deletion recovery policy.
- Backup encryption and key-management ownership.
- Recovery point objective and recovery time objective.
- Separate backup credentials and access controls.
- Monitoring and alerting for backup success, age, and restore failures.
- A recovery environment isolated from normal application traffic.

## Recovery procedure

1. Declare the incident and assign an incident owner.
2. Preserve request IDs, audit events, deployment identifiers, and relevant operational logs.
3. Stop or isolate affected write paths if continued writes could worsen corruption or privacy exposure.
4. Confirm the last known-good database backup and private-storage recovery point.
5. Restore into an isolated recovery environment using deployment-injected credentials.
6. Apply the repository migration process and verify migration state before serving traffic.
7. Verify account access, role resolution, matter ownership, document authorization, privacy queues, audit visibility, and notification integrity.
8. Confirm external integrations are either healthy or fail closed; do not enable unverified providers during recovery.
9. Run smoke tests and security checks in the recovery environment.
10. Obtain operations/security approval before directing traffic to the recovered service.
11. Record the incident, recovery point, data loss assessment, and follow-up actions.

## Restore verification checklist

- `python manage.py migrate --plan` reviewed.
- `python manage.py check --deploy --settings=config.settings.production` passes with deployment configuration.
- Database readiness and cache readiness pass.
- Private documents remain inaccessible without an authorized matter relationship.
- Passwords, tokens, and private document contents are absent from logs.
- Audit events retain bounded request correlation.
- Backups remain protected from application write credentials.

Recovery testing must be completed and recorded by the production operations owner before launch.
