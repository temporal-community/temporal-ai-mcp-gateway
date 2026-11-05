---
Name: Proactive Outreach for Known Issues
Owner: Ines Duarte
Status: Approved
Last Updated: 2026-04-27
---

## Context

When we know a defect affects a specific set of accounts, we wait for them to contact us. The customers who do contact us are a minority, and the ones who do not are left with a broken experience and their own conclusions about our quality.

## Proposal

Identify affected accounts and contact them before they contact us.

- Affected account identification as a required step in incident and defect handling
- A message that states what happened, what we did, and whether action is needed from them
- Sent once, with no follow-up unless they reply
- Support briefed before the message goes out, not after

## Scope

Defects with a determinable affected set. Broad outages use the status page and the existing incident communication.

## Risks

Telling people about a problem they did not notice creates contacts that would not otherwise exist, and for minor issues the cure is worse than the disease. A threshold on impact is needed, and the default for cosmetic issues should be silence.

## Measurement

Affected accounts contacted before contacting us, reply rate, inbound volume following an outreach, and satisfaction among contacted accounts against a comparable set.

## Dependencies

Identifying the affected set is the work, and it differs per defect. Some are a query over the events the bug touched; others mean reconstructing which accounts hit a code path that no longer runs.

- A retained signal per defect class that keeps the affected set recoverable after the fix ships
- A sending path that reaches the right person, which for a workspace means choosing between the administrator and the affected member
- A record of who was contacted and why, since a second outreach to the same account in a month is a different decision from the first

## Operational Impact

The required step lands on incident handling, already the busiest moment. Identifying a set during the incident is both the right time and the worst time, so the requirement is to record how the set could be identified, with the list assembled once the fix is out. Briefing support first is the other load: an outreach that reaches customers before the queue has context produces exactly the confusion it was meant to prevent.

## Open Questions

- Where the impact threshold sits, which the first few cases will have to settle rather than anyone writing a number now
- Whether an account that already contacted us is included, excluded, or sent something different
- Who writes the message, given support knows the customers and engineering knows the defect
- Whether the threshold reads severity or duration, since a small defect running a month and a large one running an hour differ
