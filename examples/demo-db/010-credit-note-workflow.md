---
Name: Credit Note Workflow
Owner: Ben Tsai
Status: In Review
Last Updated: 2026-01-08
---

## Background

Credit notes are issued through a console form that writes directly to the invoice record. There is no approval step, no reason taxonomy, and no link back to the thing that went wrong, so the monthly credit total is a number nobody can decompose.

## Proposal

Make credit notes a first-class object with a short workflow in front of them.

- A required reason from a fixed list, with free text as a supplement rather than a substitute
- Approval above a threshold, routed by amount rather than by role
- A link to the originating case, incident, or order
- Credits appear on the next statement with the reason visible to the customer

## Scope

Customer-facing credits only. Internal write-offs and bad debt stay with finance and their existing process.

## Risks

Adding approval adds latency to an apology, which is exactly the wrong place to add latency. The threshold matters more than the workflow: set it too low and every goodwill gesture waits on a manager. We propose starting high and lowering it only if the data shows a problem.

## Measurement

Credits by reason as a share of revenue, median time from decision to credit visible, and the share of credits with a usable link to their cause, which today is near zero.

## Data We Have

Last year's credits can be partly reconstructed from the free-text field, and that reconstruction is why this proposal exists. About half the entries name a case number in some format, a quarter say something like goodwill, and the rest are blank. The reason list should be built from the readable half rather than invented: five reasons cover nearly all of them, and a sixth catch-all beats a list long enough that people pick the first plausible entry.

- Credits run about nine hundred a month, weighted heavily to a few large accounts
- Roughly half carry a case number that can be matched automatically
- The amount distribution is bimodal, which is what makes a single threshold workable

## Interfaces Affected

The console form writes to the invoice record directly, so the credit object has to become the only writer and the form has to go through it. Anything else leaves a second path producing credits with no reason attached, which is today's state with extra steps. The statement renderer also gains the reason text, so reason names are customer-visible and have to read as explanations rather than internal categories.

## Open Questions

The starting threshold has no number. Above the upper mode, approval almost never fires, which is safe and may make the workflow pointless. Between the modes it catches a meaningful share and slows a lot of small apologies. Nobody has said which failure they would rather have for the first quarter.
