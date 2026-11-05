---
Name: Promoted Listings Placement
Owner: Yusuf Demir
Status: Draft
Last Updated: 2026-02-03
---

## Context

Promoted listings appear inline with organic results, marked with small text that our own testing shows most buyers do not notice. The revenue is meaningful. The buyer experience is a search result that is not ranked by what we told buyers it is ranked by.

## Proposal

Separate promoted placement visually and bound it numerically.

- A maximum of two promoted listings per result page, placed in a distinct block
- Labeling that is legible rather than minimal, tested for whether people actually register it
- Promoted listings subject to the same availability and quality filters as organic results
- Buyer outcome tracking on promoted placements specifically, including returns

## Non-goals

No change to the auction mechanics or to pricing, which are owned by the advertising team.

## Risks

Clearer labeling and fewer slots will reduce promoted revenue, which is a real cost to put against a diffuse benefit. The argument rests on the marketplace being worth more when buyers trust the results, which is true and is difficult to demonstrate within a quarter.

## Measurement

Promoted revenue, buyer recognition of the label in testing, return and dispute rates on promoted versus organic purchases, and repeat purchase rate as the long-term signal.

## Alternatives Considered

Keeping promoted listings inline and only improving the label is cheaper and is what the advertising team prefers. It fails the test the proposal sets: a label that registers inside a list people are scanning has to be large enough to break the scan, at which point visual separation exists anyway, just badly. Moving promoted listings into a block below the first screen protects organic results completely and costs far more revenue than two slots at the top, which makes it a harder trade rather than a safer version of this one.

## Sequencing

Label testing runs before anything ships, because both the slot count and the placement depend on what buyers actually register. Running it afterwards turns the test into a justification exercise.

- Label variants tested with buyers first, measuring recognition rather than preference
- The quality and availability filters applied to promoted listings next, which is correctness work and does not wait on layout
- Slot count and block placement last, with promoted revenue read weekly through the change

## What Would Change Our Mind

If return and dispute rates on promoted purchases come out no worse than organic, the quality filter is the whole fix and the placement change is cosmetic. The case for two slots rests on promoted results being measurably worse purchases, and that is checkable before shipping the part that costs revenue.
