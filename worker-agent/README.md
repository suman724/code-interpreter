# worker-agent

gRPC service running on worker nodes. Wraps Microsandbox to create sandboxes, run code, and perform native file IO.

## Quickstart
- Configure Microsandbox endpoint and workspace root.
- Start gRPC server.

## Configuration
See `CONFIG.md`.

## Tests
- `make lint`
- `make type`
- `make test`
