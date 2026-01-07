# worker-agent Architecture

## Responsibilities
- Implement WorkerService gRPC API.
- Create and stop sandboxes via Microsandbox JSON-RPC.
- Execute code/commands and return results.
- Provide streaming file upload/download (PutFile/GetFile).
- Enforce path sanitization and workspace quotas.

## Key data flows
- **StartSession**: create workspace → call `sandbox.start` → store sandbox id.
- **ExecuteCode/RunCommand**: forward to Microsandbox and return stdout/stderr/exit.
- **PutFile/GetFile**: stream data to/from workspace with size limits.

## Failure modes
- Microsandbox unavailable → return gRPC UNAVAILABLE.
- Disk full → return RESOURCE_EXHAUSTED.
- Invalid paths → return INVALID_ARGUMENT.

## Scaling considerations
- Prefer local NVMe storage.
- Limit concurrent transfers to prevent IO starvation.
