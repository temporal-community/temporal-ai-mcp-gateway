---
Name: Card Network Fee Reporting
Owner: Dmitri Volkov
Status: Draft
Last Updated: 2025-12-03
---

## Context

Interchange and scheme fees arrive as a monthly file with four hundred line types and no mapping to our transactions. Finance allocates them across products by volume, which is a reasonable approximation and wrong in ways that matter when a product's mix shifts.

## Proposal

Match fee lines to transactions where the file permits it, and make the unmatched remainder explicit.

- A parser per scheme, versioned, because the file formats change without notice
- Matching on the processor reference where present, falling back to amount and date windows
- Unmatched fees allocated as today but reported separately and visibly
- A monthly report of fee per transaction by product, region, and method

## Non-goals

No attempt to optimize routing or negotiate rates. This is measurement, and the optimization conversation needs the measurement first.

## Risks

The match rate will be mediocre for at least two schemes, and a mediocre match rate presented as precision is worse than the honest approximation we have now. The report leads with coverage and only then with numbers.

## Measurement

Share of fees matched to a transaction, variance between allocated and matched cost per product, and whether the first optimization decision made from this data survives contact with the next month's file.

## Failure Modes

- A format change ships without notice and the parser produces plausible rows instead of an error, which is the dangerous shape: a file parsed into the wrong line types still reconciles to a total
- Amount-and-date-window matching produces false matches on high-volume days where many transactions share an amount, and a false match is invisible in aggregate
- A scheme that back-dates adjustments into a closed month moves the matched share for a month already reported, so the report needs a restatement path rather than one final figure

The file total is the number that must always reconcile. Parser output that does not sum to it fails the run rather than publishing.

## Dependencies

Processor references exist on our side only for transactions after the processor migration eighteen months ago. Anything older matches by window or not at all, which caps the achievable rate on any historical comparison. That ceiling belongs in the first report rather than being discovered inside it.

## Timeline

One scheme end to end before the others, chosen for reference coverage rather than for size of spend. That produces a real match rate on real data within a month and settles whether the approach is worth extending. The remaining parsers are mechanical once the matching and reporting shape exists, and can be written in whatever order finance prefers.
