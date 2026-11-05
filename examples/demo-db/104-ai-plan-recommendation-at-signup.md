---
Name: AI Plan Recommendation at Signup
Owner: Ruth Adeyemi
Status: Draft
Last Updated: 2025-10-12
---

## Context

People choose a plan at signup with no information about which fits. Roughly eighteen percent change plan within sixty days, which suggests the initial choice is close to a guess, and each change is a support interaction or a billing adjustment.

## Proposal

Recommend a plan from the few things we know at signup, using an explicit rule set rather than a learned model.

- Three inputs: expected team size, whether single sign-on is required, and the primary use selected
- A rule table mapping input combinations to a recommended plan, reviewed quarterly with the pricing owner
- The recommendation shown with its reasons, and never preselected in the form
- All plans remain visible and selectable, in the same order, regardless of recommendation

## Non-goals

No learned model. The rule table is auditable, explainable to a customer, and changeable by the pricing owner without engineering involvement, which matters more here than accuracy at the margin.

## Risks

A recommendation carries authority the inputs do not justify: three answers cannot really predict what a team will need. Showing the reasons alongside the recommendation is what lets someone disagree with it sensibly, and the reasons must be the actual rule rather than a pleasant restatement.

## Measurement

Plan changes within sixty days, recommendation acceptance rate, and revenue per signup as a guardrail against recommending too cheaply.

## Data We Have

The eighteen percent covers changes in both directions, and the split matters: two thirds move up, one third moves down. A rule table built to minimize total changes would recommend higher plans, cutting the upward moves and flattering the revenue guardrail while leaving people on plans they did not need. The honest target is downward changes, and the measurement should separate them.

- Expected team size is already collected and is wrong often enough to be treated as a range
- The single sign-on answer is the strongest single predictor of eventual plan
- Primary use has eleven options, four of which are picked by nine in ten people

## Operational Impact

The pricing owner takes on a responsibility they do not have today. A table that goes stale between quarterly reviews recommends against the current price list. The review has to be a scheduled obligation with a named owner, and a plan change made outside it should invalidate the table until it is reviewed rather than letting it recommend a plan that no longer exists.

## Rollback

Removing the recommendation is a display change and costs nothing, which is what never preselecting it buys. There is no state to unwind, no accounts created under a rule that must be honored, and no migration. That is worth stating, because it is what makes trying this cheap.

## Open Questions

What the recommendation says when the three inputs do not reach a clear answer is undecided. Showing nothing is honest and leaves the person where they started; showing two plans with their tradeoff is more useful and harder to write in the space available.
