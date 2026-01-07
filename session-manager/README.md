# session-manager

Stores session/execution metadata and routing. Enforces TTL and idle expiration.

## Quickstart
- Configure DynamoDB tables and TTL settings.
- Run the service and start the reaper job.

## Configuration
See `CONFIG.md`.

## Tests
- `make lint`
- `make type`
- `make test`
