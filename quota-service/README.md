# quota-service

Enforces per-tenant and per-user rate limits and concurrency quotas.

## Quickstart
- Configure backing store (DynamoDB or Redis).
- Run service and integrate with the control-plane API.

## Configuration
See `CONFIG.md`.

## Tests
- `make lint`
- `make type`
- `make test`
