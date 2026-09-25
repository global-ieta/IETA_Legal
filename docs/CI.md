# Continuous integration

The repository workflow at `.github/workflows/ci.yml` runs on pushes and pull requests. It installs development dependencies, runs Django system checks, smoke-checks the production settings with non-secret CI values, detects migration drift, executes the in-memory test suite, and compiles Python modules.

The workflow does not require Global IETA, AURA, database, storage, WebRTC, or other production credentials. Those integrations remain behind mocks and interfaces during CI.

The production smoke check uses explicit CI-only values and SQLite with `ALLOW_PRODUCTION_SQLITE=true`; this is only for settings validation and does not relax the production deployment requirement for an external database.
