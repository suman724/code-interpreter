# infra-aws Architecture

## Responsibilities
- Provision networking, compute, and security per design.
- Configure ALB, EKS, and worker ASG.
- Set up Cloud Map and VPC endpoints.

## Failure modes
- Misconfigured security groups → connectivity failures.
- Missing VPC endpoints → blocked pulls/logging.

## Scaling considerations
- Separate node groups for control plane and workers.
- Use autoscaling policies tied to worker utilization.
