---
Name: Bug Report Quality from Support
Owner: Ben Tsai
Status: Draft
Last Updated: 2025-11-08
---

## Background

Bugs reported by support reach engineering with a customer description and little else. Engineering sends about half back for more information, which takes days and frequently means asking the customer, who has moved on.

## Proposal

Capture the diagnostic context at the moment of the report rather than after.

- A report form requiring account identifier, timestamp, and the exact steps as described
- Automatic attachment of the session trace and recent errors for that account
- A reproduction attempt by support before submission, with the result recorded either way
- Reports missing required context returned by the form rather than by an engineer

## Scope

Bugs raised from support tickets. Internally discovered bugs follow the normal path.

## Risks

Automatic trace attachment means pulling customer session data into an engineering system, which has a privacy treatment that needs settling before implementation. Scope the attachment to the specific session window rather than the account's history.

## Measurement

Reports returned for more information, time from report to engineering acknowledgement, and the share of reports with a successful support reproduction.

## Support Impact

The reproduction attempt is the expensive part. It moves roughly fifteen minutes per report from engineering to support, onto a queue that is already the constraint. It is still the right trade, because the attempt happens while the customer is still reachable, but it has to be funded rather than absorbed quietly. A reproduction that fails is a real result and should not count against a rep's handle time.

## Dependencies

- Session trace retention long enough to cover the gap between the customer hitting the bug and support filing it, which is shorter than that gap on some tiers today
- A privacy decision on what may cross into the engineering system, which blocks implementation rather than design
- Account resolution from a ticket, still manual when the customer writes in from an address not on the account

## Open Questions

Whether the form may reject a report at all while the customer is on the phone and the rep has no timestamp to give it. Returning the report protects the engineering queue and risks the bug never being filed, and an unfiled bug is the outcome none of the proposed measures would show.

## Timeline

The form and its required fields can ship in three weeks and are worth having on their own. Trace attachment waits on the privacy decision and should not be scheduled until that lands. The reproduction step goes last, after support has seen that the form reduces the questions coming back at them.
