# scheduler Architecture

## Responsibilities
- Track worker heartbeats and health.
- Implement placement algorithm (bin-pack).
- Return worker endpoints to Session Manager or API.

## Key data flows
- **AllocateSession**: choose a worker based on CPU/RAM headroom and AZ.
- **Heartbeat**: ingest worker stats and mark stale workers.

## Failure modes
- No healthy workers → return capacity errors.
- Stale discovery data → return 503 and force re-sync.

## Scaling considerations
- Partition scheduler state by AZ.
- Cache Cloud Map results with short TTL.
