# quota-service Architecture

## Responsibilities
- Enforce session creation limits and execution rate limits.
- Track counters per tenant and optional per user.
- Provide allow/deny responses to the control plane.

## Key data flows
- **CheckQuota**: evaluate current counters + config limits.
- **RecordUsage**: increment counters for sessions/executions.

## Failure modes
- Store unavailable → fail closed for high-risk actions.
- Counter drift → periodic reconciliation or reset windows.

## Scaling considerations
- Use sharded counters for high-traffic tenants.
- Prefer Redis for low-latency rate limits.
