---
Name: Funnel Drop-Off Diagnostics
Owner: Omar Haddad
Status: Draft
Last Updated: 2026-01-22
---

## Background

The funnel tells us where people stop. It does not tell us anything about why, so the next step is always the same: an analyst segments the drop-off group by whatever they think might matter and looks for a difference.

## Proposal

Automate the first pass of that segmentation.

- For a selected drop-off step, compute the difference in attribute distribution between those who continued and those who did not
- Rank attributes by the size of the difference, with a significance threshold
- Present the top differences as a starting list, with the sample sizes beside them
- Link each attribute to the underlying population for manual inspection

## Scope

Attributes already present in the account and session model. No new collection.

## Risks

Ranking by difference finds correlations, and most of them are consequences rather than causes. Presented as a list of reasons, this would produce confident conclusions about things that are merely associated with the real cause. The presentation has to be explicit that these are places to look, not explanations.

## Measurement

Time from identifying a drop-off to having a hypothesis, the share of hypotheses that survive a follow-up test, and analyst use of the feature relative to doing it by hand.

## Review Notes

- Ranking every attribute at once is a multiple-comparison problem, and a threshold applied independently per attribute will surface spurious differences at a predictable rate; the correction belongs in the computation rather than in a caveat under the list
- Plan tier, seat count, and billing amount move together, so the top of the ranked list will frequently be the same finding wearing three names
- The sample sizes beside each row carry most of the honesty in this presentation and should not be collapsible
- Attributes that are only set after the step in question are consequences by construction and should be excluded, not ranked

## Interfaces Affected

Only the funnel view changes, and it gains a panel rather than a page. The quieter consequence is that the account and session model becomes a surface people read: any attribute added for an unrelated reason starts appearing in this ranking the same day, including internal flags that were never meant to be shown to anyone outside the team that set them.

## What Would Change Our Mind

If the hypotheses analysts form today already survive follow-up tests most of the time, the first pass is not where the time goes and this builds a faster version of the step that was never slow. A week of shadowing would tell us where the hours actually sit, and it should happen before the build rather than after the adoption number disappoints.
