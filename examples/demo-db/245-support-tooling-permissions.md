---
Name: Support Tooling Permissions
Owner: Victor Alves
Status: Approved
Last Updated: 2026-03-29
---

## Problem

Everyone in support has the same permissions, which include viewing account content, issuing refunds without limit, and impersonating a user. Most of the team needs none of those for most of their work, and our last access review flagged this as the largest single excess in the company.

## Proposal

Permissions by role and by case, with the sensitive capabilities gated.

- Three roles reflecting what people actually do, replacing the single role
- Content viewing requiring an open ticket with that account, logged per view
- Impersonation requiring customer consent recorded on the ticket, with a time limit
- Refund authority bounded by role, with the existing discretion path for exceptions

## Scope

The support console. Engineering access to production follows the just-in-time work.

## Risks

Gating content viewing on an open ticket breaks the legitimate case of investigating a pattern across accounts, which the quality and fraud functions do regularly. Those need a separate, logged, reviewed path rather than being forced to work around the gate.

## Measurement

People holding each capability, content views without an associated ticket, impersonation sessions per month, and support resolution time, watched for whether the gates are costing us.

## Migration

Everyone holds the single role today, so the cutover is a mapping exercise rather than a grant exercise. Managers place each person into one of the three roles from the existing team roster, and anyone unmapped on the cutover date lands in the most limited role rather than the most permissive one. That will misplace some people on day one, and the cost is a burst of escalations in the first week while mappings get corrected.

- Roster mapping drafted by managers two weeks before cutover and reviewed by the access review owner
- Refund ceilings set per role from the last twelve months of refund amounts, not from estimates
- Impersonation left ungated for the first week so consent capture can be watched before it blocks anyone

## Failure Modes

The gates fail in two directions. A ticket closed while an investigation is still running revokes content viewing partway through, and the responder has no way back except reopening the ticket, which distorts resolution time. A stale open ticket does the opposite, keeping content viewing alive long after the work finished, which moves the excess the access review flagged rather than removing it. Per-view logging catches that second case only after the fact.

## Open Questions

- Whether the quality and fraud path is a fourth role or a request-and-approve grant layered on an existing role
- How long an impersonation session should run before it expires, given consent is recorded once per ticket
- Whether refund authority is bounded per refund, per day, or both
