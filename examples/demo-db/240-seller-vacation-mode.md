---
Name: Seller Vacation Mode
Owner: Dana Whitfield
Status: Approved
Last Updated: 2026-05-29
---

## Context

Sellers who take time off either leave listings active and miss orders, which damages their performance metrics, or delete listings and rebuild them, which loses their history. Several have told us they simply do not take time off, which is not a sustainable position for a business we depend on.

## Proposal

A vacation mode that suspends selling without suspending existence.

- Listings hidden from search and browse, with direct links showing an away notice and a return date
- Performance metric windows paused for the duration
- Dispute and return deadlines paused, which the dispute work depends on
- Automatic return on the stated date, with a reminder beforehand

## Scope

Seller accounts. Open orders at the point of activation remain the seller's responsibility and the mode should say so plainly.

## Risks

Pausing dispute deadlines is open to abuse by a seller activating vacation mode to escape a dispute window. Restricting activation while a dispute is open covers the obvious case and should be stated in the policy rather than enforced silently.

## Measurement

Sellers using the mode, orders missed during absences, performance penalties applied during absence, which should reach zero, and disputes opened immediately before activation.

## Interfaces Affected

Pausing a metric window changes how performance is computed rather than what the display reads. The metric service calculates rolling windows over wall-clock time, and vacation days have to leave the denominator rather than count as days with no activity. That is a change in a service several teams read from, and anything caching a computed score will hold a stale one across the pause boundary.

- Metric windows become seller-relative rather than wall-clock
- Search and browse need an exclusion that does not look like a deletion to the index
- Dispute and return timers need an explicit paused state, which they do not have today

## Failure Modes

Automatic return on the stated date assumes the seller is ready. Someone who extends their absence without updating the date comes back to active listings with nobody minding them, which is the failure this exists to prevent and is now worse because they believed they were covered. The reminder before return has to allow extending from the reminder itself, in one action, rather than sending them to a settings page.

## Rollout

Restricting activation during an open dispute lands with the first release rather than later. It is the one piece whose absence is exploitable, and adding the restriction after sellers have used the feature without it reads as a withdrawal rather than a policy.
