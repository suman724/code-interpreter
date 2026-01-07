# sdk-python Architecture

## Responsibilities
- Typed wrappers for REST endpoints.
- Helpers for upload/download and streaming.
- Retry and idempotency support.

## Failure modes
- Network timeouts → retry with backoff.
- 429 responses → surface quota errors.

## Scaling considerations
- Use connection pooling.
