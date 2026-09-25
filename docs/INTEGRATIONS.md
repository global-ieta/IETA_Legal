# Integration boundaries

Awaiting official integration contracts:

- Global IETA authentication and identity claims
- AURA API, authentication, model, request/response schema
- Production database and connection policy
- Private document storage
- Document malware/content scanning
- Email and SMS delivery
- TURN/signaling provider for WebRTC
- Payments, if the owner later approves that scope

Authentication selection is now explicit: development uses the local Django provider; production defaults to a fail-closed Global IETA provider. The provider interface is stable so templates, portals, permissions, and workflows do not depend on the external identity transport.

Each item must be implemented as a client plus adapter behind a stable application interface. Secrets belong in deployment environment configuration and never in source control.

The AURA boundary now includes `AuraClient`, `OfficialAuraProvider`, internal request/response dataclasses, and the development mock. The official client intentionally raises an unavailable error until the owner supplies the real contract. Any `AI_PROVIDER` value other than `aura` is rejected.

Global IETA now has the equivalent `GlobalIetaClient`, `OfficialIdentityProvider`, identity dataclasses, and development mock boundary. Supplying partial identity configuration does not cause a fabricated request; the official path is selected only when all required configuration values exist.

Calling now has the same explicit boundary: `SignalingProvider`, `MockSignalingProvider`, and `OfficialSignalingProvider`. The development provider creates only a local session identifier and records `media_transmitted: false`; it never handles audio or video. Supplying both `CALLING_API_BASE_URL` and `CALLING_API_KEY` selects the official adapter, whose unimplemented client fails closed until the owner supplies the signaling/TURN contract.

The participant-scoped `/calls/status/` endpoint can be used by a future client to observe local call state. It does not imply that WebRTC media, TURN allocation, recording, emergency handling, or provider health checks are implemented.

Private documents now have a `DocumentSafetyProvider` boundary. The development provider performs no content inspection and marks each upload `manual-review-required`; the official adapter fails closed until the owner supplies scanner transport, result fields, and approval policy. If official scanning configuration is present, new uploads are not stored and admin approval is blocked.

Private storage has a separate `PrivateStorageProvider` boundary. Local filesystem storage is operational only for development and has no public URL. Selecting a cloud backend before its adapter is implemented blocks uploads and reports `contract-pending`; production settings reject local storage unless an explicit development override is supplied.

Notification creation is centralized through `create_in_app_notification`. The notification-delivery boundary currently guarantees only recipient-scoped in-app notifications; configuring an external delivery endpoint reports `contract-pending` and does not claim that email or SMS was sent.

The notification centre exposes this boundary to users. External delivery would require both an operational provider and the user’s `notifications` consent; neither is treated as sufficient until the delivery contract is implemented.
