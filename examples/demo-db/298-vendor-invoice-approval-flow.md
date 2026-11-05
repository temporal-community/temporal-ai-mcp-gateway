---
Name: Vendor Invoice Approval Flow
Owner: Felix Braun
Status: Draft
Last Updated: 2026-04-08
---

## Problem

Vendor invoices arrive by email to finance, who forward them to whoever they think owns the relationship. Approvals come back as replies, and the audit trail is a mailbox. Late payments are common and the cause is almost always a forwarded message that nobody answered.

## Proposal

Structured intake with routing from the vendor record and a visible approval state.

- Invoices matched to a vendor record with a named internal owner
- Approval requested in a tool with a due date and escalation on inaction
- Purchase order matching where one exists, flagging variance rather than silently paying
- Payment status visible to the owner, so chasing finance is unnecessary

## Scope

Vendor invoices. Employee expenses follow the expense tooling path.

## Risks

Escalation on inaction will route approvals upward to people who have no context, who will approve to clear the queue. The escalation should go to a named finance approver rather than up a management chain, which turns an absent approval into a finance decision rather than a rubber stamp.

## Measurement

Invoices paid by due date, time in approval, escalations triggered, and variance flagged against purchase orders.

## Rollout

Start with the forty vendors that account for most invoice volume, because those records already carry a named internal owner in the vendor master. Everything else keeps arriving in the finance mailbox until the missing owners are filled in. Running both paths at once means finance watches two queues for a quarter, which is the cost of not blocking this work on a vendor data cleanup nobody owns.

- Weeks 1-4: structured intake and vendor matching, approvals still by reply
- Weeks 5-8: approval state, due dates, and escalation for the top vendors
- Weeks 9-12: purchase order matching and variance flagging

## Interfaces Affected

Once intake stops being an email thread, three systems change shape. The vendor master gains a required internal owner field, and a vendor without one cannot be matched. The payment run reads approval state instead of a finance analyst's notes. Purchase orders have to be queryable by vendor and number at intake time, which procurement supports but has never been asked to do at this volume.

## Open Questions

Credit notes and partial invoices have no settled path. A credit note has no due date and no purchase order to match against, so it either skips approval or borrows the owner of the invoice it offsets. Nothing is decided for invoices matched to a vendor whose internal owner has left the company; finance guesses today, and this proposal does not say who guesses instead.
