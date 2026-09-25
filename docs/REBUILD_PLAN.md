# IETA Legal rebuild plan

## Current state

The repository began with no application source, dependency manifest, or database schema. The foundation is now a Django 4.2 project with server-rendered templates, a Tailwind-compatible token layer, modular app boundaries, and no external credentials.

## Target architecture

`config/` owns environment-specific settings and routing. Business responsibilities are separated into `accounts`, `users`, `advocates`, `intake`, `matters`, `aura`, `consultations`, `messaging`, `calling`, `privacy`, `audit`, `dashboard`, and `public_site`. `integrations/` contains replaceable Global IETA and AURA interfaces/mocks.

## Keep / refactor / replace

There was no prior product code to preserve. The initial implementation is the replacement foundation. Future integration work should keep domain models and service interfaces while replacing only the mock adapters and deployment configuration.

## Risks

- Official Global IETA, AURA, storage, email/SMS, payments, and TURN contracts are not supplied.
- Demo sessions are deliberately not production authentication.
- WebRTC signaling is represented as an architecture boundary, not a production call service.
- Product legal language, privacy retention, advocate onboarding, and fee workflows require qualified review.

## Phases

1. Foundation and public site (implemented)
2. Demo roles and distinct portals (implemented)
3. Intake, matter, advocate, consultation, and privacy models (implemented foundation)
4. Development end-to-end intake → advocate choice → pending conflict check (implemented)
5. AURA interface and safe mock (implemented)
6. Messaging, calling, audit, and object-level authorization hardening (foundation present; expand with official contracts)
7. Production identity, database, storage, observability, and deployment after owner supplies contracts.

The development workflow includes an idempotent `seed_demo_workspace` command for exploring the complete sample journey without inventing real-world users or advocates.
