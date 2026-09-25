# Testing notes

The current suite covers:

- Django system-check-compatible URL and template wiring
- development-role entry and production disablement
- factual-only AURA mock behaviour
- user-to-user matter ownership checks
- portal access requiring a simulated role
- Django admin remaining separate from the demo role session
- consultation acceptance/decline relationship checks
- conversation read/write isolation and notification creation
- notification recipient isolation and read-state transitions
- admin document approval/rejection boundaries
- pending private documents remaining unavailable
- versioned privacy consent and non-destructive privacy requests
- username/email authentication, password hashing, registration, logout, provider failure, and response validation
- authentication redirects, portal role boundaries, rate limits, and production configuration validation

Run `python manage.py test` for the default development database or `python manage.py test --settings=config.settings.testing` for the in-memory test configuration. The current suite contains 93 tests. Before production, add integration tests for the official Global IETA identity adapter, AURA contract, private document storage, notifications, signaling, and every object-level access policy.
