---
Name: Buyer Review Moderation
Owner: Felix Braun
Status: Approved
Last Updated: 2026-06-29
---

## Problem

Reviews are moderated on report only. Sellers report reviews they dislike, moderators are inconsistent about what breaches policy, and the perception among sellers is that reporting works if you do it often enough, which is corrosive.

## Proposal

Clear policy, consistent application, and transparency about outcomes.

- A published policy covering what will and will not be removed, with examples
- Automated detection of the clear breaches, which is personal data and abusive language
- Reports handled against the policy with a reason given to both parties
- Removal rates published per category, so the process is visible

## Scope

Buyer reviews of sellers and items. Seller ratings of buyers are a separate and smaller problem.

## Risks

Publishing the policy tells bad actors exactly how close to the line they may go, which is the standard tradeoff and worth it here, since the current opacity is doing more harm. Automated detection of abusive language performs badly across languages and dialects, and over-removal in a language the moderators do not read is a failure nobody will notice.

## Measurement

Reports per thousand reviews, removal rate against policy categories, appeal rate and outcome, and removal rate by language, watched for the over-removal case.

## Staffing

Moderation headcount does not change, but the work does. Today moderators decide; under the policy they apply it, and the hard cases become escalations with a named owner. The gap is language coverage. We moderate in six languages and receive reviews in more than thirty, so detection in an unread language has no human check behind it. Either those languages route through translation before removal, or detection is limited to the six and the rest stays report-only until coverage exists.

## Rollout

- Policy published two weeks before anything changes, so sellers see the rules before the enforcement
- Personal-data detection first, the category with least disagreement about what counts
- Abusive-language detection on the six moderated languages only, with removals sampled weekly
- Published removal rates starting from the first full month, not a partial one

## Open Questions

Appeals carry no service commitment. A removal that takes an hour and an appeal that takes nine days is not a fair process however correct each decision is, and nobody has set the appeal window. There is also no decision on whether a review restored on appeal keeps its original timestamp and position or reappears as new, which matters to the seller whose average rating moved in between.
