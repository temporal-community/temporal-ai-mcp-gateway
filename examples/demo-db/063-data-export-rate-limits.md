---
Name: Data Export Rate Limits
Owner: Maya Brennan
Status: Approved
Last Updated: 2026-06-30
---

## Problem

Exports are unlimited. A handful of customers pull their entire dataset repeatedly through the day, which is within their rights as written and is also a meaningful share of warehouse load, concentrated at the hours everyone else is working.

## Proposal

Published limits with a path to more, rather than silent degradation.

- A documented rate per plan, with the current usage visible to the customer
- Large exports queued and executed off-peak, with notification on completion
- A burst allowance so occasional large pulls are not penalized
- Limits enforced per organization rather than per credential, to prevent trivial circumvention

## Non-goals

No change to what can be exported. This is about when and how fast, not about access.

## Risks

Introducing a limit where none existed is a contractual question for the accounts currently exceeding it, and those conversations should happen before enforcement rather than as a response to it. There are six such accounts and the account team needs the list now.

## Measurement

Peak-hour warehouse load from exports, accounts hitting the limit, and support escalations about export speed, which we expect to rise briefly and then settle.

## Timeline

The six accounts come first and nothing enforces until those conversations have happened.

- Week one: the six named, with their peak-hour volume, handed to the account team
- Week four: usage visible to every customer with no limit applied, so the number is familiar before it binds
- Week twelve: enforcement for new accounts, then existing accounts outside the six, then the six on negotiated terms

## Interfaces Affected

- The export endpoint, which gains a queued response shape for anything above the burst allowance
- Account settings, which has no concept of a consumption meter today
- Completion notification, which has to reach a person rather than an integration, since a queued export may finish overnight
- Organization-level accounting, because limits are per organization and billing is the only place that resolves credentials to one today

## Support Impact

The predictable escalation is an export that used to take ten minutes and now runs overnight. That is the designed behavior and it still arrives as a complaint, so a responder needs the usage, the limit, and the queue position in one view rather than three.

- Queue position and expected start time visible to the responder and to the customer
- A documented path to request more, which is an account conversation rather than a support override
- No manual queue jumping, since one exception becomes the thing every escalation asks for
