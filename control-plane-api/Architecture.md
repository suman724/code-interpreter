# control-plane-api Architecture

## Responsibilities
- Expose REST endpoints from the OpenAPI contract.
- Validate requests, enforce authN/authZ, and apply quota checks.
- Route requests to the correct worker using Session Manager routing.
- Manage idempotency for session/execution creation.
- Provide optional streaming (SSE/WebSocket) for execution events.

## Key data flows
- **Create Session**: Validate request → quota check → schedule placement → start session on worker → persist routing in Session Manager.
- **Execute Code/Command**: Resolve session routing → dispatch to worker → return stdout/stderr/status.
- **File IO**: Either presigned S3 flow or native streaming via worker.

## Failure modes
- Session Manager unavailable → fail requests with 503 and retry guidance.
- Worker unreachable → return 503; do not migrate READY sessions.
- Idempotency store unavailable → reject unsafe POSTs or degrade to at-most-once with warning.

## Scaling considerations
- Stateless HTTP nodes; scale horizontally behind ALB.
- Cache session routing with short TTL to reduce Session Manager load.
- Apply rate limits to protect downstream services.
