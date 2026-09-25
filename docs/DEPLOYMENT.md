# Deployment checklist

The repository includes a production-oriented `Dockerfile`. It runs as a non-root user, collects static assets during image creation, exposes the liveness/readiness endpoints, and starts Gunicorn. It does not contain secrets or automatically invent external service configuration.

Before deployment:

1. Supply a long random `DJANGO_SECRET_KEY` (production rejects placeholders and short values).
2. Set explicit `DJANGO_ALLOWED_HOSTS` and HTTPS-only `DJANGO_CSRF_TRUSTED_ORIGINS`; wildcard hosts are rejected.
3. Set `DEMO_MODE=False`.
4. Supply the official Global IETA identity configuration.
5. Set `AUTH_PROVIDER=global_ieta` and supply the official Global IETA identity configuration. Local authentication is not a production identity service.
6. Supply the official AURA contract/configuration, or keep AURA unavailable until it is reviewed.

Use `/health/ready/` for database/cache probes and `/health/integrations/` for a non-networking report of AURA, Global IETA, and calling configuration. A `contract-pending` integration is not production-ready merely because credentials are present.
7. Configure a non-SQLite production database through deployment environment variables and run migrations as a release step. SQLite requires the explicit `ALLOW_PRODUCTION_SQLITE=True` override.
8. Configure the private document storage adapter and malware/content scanning. Production rejects local private storage unless the explicit development override is set.
9. Configure a shared cache for rate limiting across processes.
10. Configure TLS termination, secure cookies, log collection, backups, and alerting.
11. Complete legal, privacy, security, advocate-operations, and WebRTC infrastructure review.

The current container command starts the web process only. Database migration, secret injection, and external service provisioning belong in the deployment system rather than in the image build.

Set `DB_ENGINE` to the installed Django database backend and provide `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` for a non-SQLite deployment. SQLite remains the development fallback.
