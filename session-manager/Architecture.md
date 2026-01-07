# session-manager Architecture

## Responsibilities
- Persist session and execution records.
- Store session routing (session_id → worker endpoint/sandbox id).
- Track idempotency records for POST requests.
- Enforce TTL and idle timeout expiration.

## Key data flows
- **Create Session**: Write session in STARTING, then mark READY when worker confirms start.
- **Lookup Session**: Provide routing to API for execution/file requests.
- **Reaper**: Periodically stop expired or idle sessions.

## Failure modes
- DynamoDB throttling → backoff/retry; return 503 when write capacity is exhausted.
- Stale routing entries → return 503 for worker calls and allow reaper cleanup.

## Scaling considerations
- Use partition keys by tenant_id for scale.
- Enable DDB TTL on sessions/executions.
- Use conditional writes for idempotency.
