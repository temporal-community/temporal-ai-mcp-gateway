---
Name: Customer Satisfaction Survey Redesign
Owner: Jonas Keller
Status: Draft
Last Updated: 2025-10-08
---

## Background

We survey after every resolved ticket with a five-point scale and an optional comment. Response rate is eleven percent and skews toward the extremes, which means the score tracks the volume of angry customers rather than the quality of support.

## Proposal

Ask less, ask better, and sample rather than survey everyone.

- A single question about whether the issue was resolved, with the rating secondary
- Sampled at thirty percent of resolutions rather than sent to all, to reduce fatigue
- Follow-up question branching on the answer rather than one form for everyone
- Comments routed to the person who handled the ticket, which currently does not happen

## Non-goals

No change to the public-facing review solicitation, which is a marketing surface with different objectives.

## Risks

Sampling reduces volume and therefore increases noise in per-person and per-queue breakdowns, which some managers use. Being explicit about what the sample can and cannot support is necessary, since a thin sample sliced finely will produce confident nonsense.

## Measurement

Response rate, distribution shape against the current extremes, and whether the resolution question correlates with reopened tickets, which is our only objective check on it.

## Data We Have

Two years of responses at eleven percent is enough to model what a thirty percent sample does to the per-queue breakdowns before any manager loses a number they rely on. Reopened-ticket rates are already joined to tickets in the warehouse, so the correlation check can run retrospectively against the existing five-point answers rather than waiting a quarter.

- Responses per queue per week, which sets the floor for how finely a sample can be sliced
- Comment text that no one who handled the ticket has ever read
- Response rate by channel, which differs by a factor of three and will skew an even sample

## Sequencing

The sampling change and the question change should not ship together. Sampling first, with the existing five-point question, isolates its effect on response rate and distribution. The new question follows a month later, so a shift in the score belongs to one change or the other. Shipping both at once makes the first month uninterpretable, and this survey has no second source to check it against.

## Support Impact

Routing comments to the person who handled the ticket is the part the team will feel. Comments are an anonymous aggregate today, and this makes both praise and complaint personal on the same day.

- The handler sees the comment text, and so does the manager, rather than a summary
- A rule that one comment is not a performance conversation, written down before the first one lands
- Queue reporting carries the sample size, so a thin week reads as thin and not as a drop
