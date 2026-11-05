---
Name: Office Access Badge Audit
Owner: Sofia Marchetti
Status: Draft
Last Updated: 2025-08-30
---

## Context

Badge access is granted at onboarding and revoked at offboarding, in theory. An informal check found active badges for eleven people who have left, and several contractor badges with no expiry and no record of who approved them.

## Proposal

Reconcile badges against the staff record and keep them reconciled.

- A quarterly reconciliation between the badge system and the staff directory
- Contractor badges issued with an expiry matching the contract end
- Offboarding including badge revocation as a verified step rather than an assumed one
- Access by area reviewed against role, since several areas are open to everyone by default

## Scope

Physical access badges across all offices.

## Risks

The reconciliation will find badges belonging to people whose status is ambiguous, such as those on extended leave or in a notice period, and the right handling differs per case. A default of suspend rather than revoke covers most of these without being punitive.

## Measurement

Badges without a matching active staff record, contractor badges with an expiry, revocation completed at offboarding, and areas with role-appropriate access.

## Dependencies

The staff directory is the reference and it is incomplete for contractors: each hiring manager tracks engagements in whatever form they prefer, which is why those badges have no end date to match. Reconciling against a record that omits many holders produces a long exception list and no improvement.

- Contractor engagements recorded in the directory with an end date, before the first reconciliation
- The badge system exporting holder, area, issue date, and approver, which it does for three of the four offices
- An identifier that joins a badge to a person, since the badge system keys on a name string today

## Operational Impact

The eleven known cases are revoked now, separately from the process work, because waiting a quarter to close a finding nobody disputes is how it reappears in the next review.

- Offboarding gains a verified step, meaning a person confirms the badge is dead rather than a checklist being ticked
- Facilities carries the reconciliation, roughly two days of work per round
- Suspend rather than revoke needs a badge state that supports it, which exists, and a route back for a returner

## Timeline

Contractor records and the badge export first, six weeks, since nothing is trustworthy without them. The first full reconciliation the quarter after, with its exception list read as a baseline, not a failure. Area access against role last, because it touches every team and changes what people can do rather than who holds a badge.
