# control-plane-api

Public HTTP API for session-based code execution. Handles authN/authZ, request validation, quotas, session routing, idempotency, and streaming.

## Quickstart
- Configure service dependencies (Session Manager, Scheduler, Quota Service, Worker gRPC endpoint).
- Start the API server.

## Configuration
See `CONFIG.md`.

## Tests
- `make lint`
- `make type`
- `make test`
