---
Name: Dashboard Load Performance
Owner: Ines Duarte
Status: In Review
Last Updated: 2026-07-17
---

## Context

The median dashboard takes six seconds to become useful and the ninety-fifth percentile takes twenty-two. The slow ones are slow for different reasons, and because we measure only total load time, every conversation about it is speculative.

## Proposal

Instrument the load path properly, then fix what the data points at.

- Timing broken into query, transfer, and render, reported per dashboard
- Attribution of total time to the slowest query rather than the sum
- A performance view available to dashboard authors, not just to the platform team
- Targets set per percentile with an agreed definition of useful

## Non-goals

No optimization work in this phase, which is deliberate. We have guessed wrong twice about where the time goes and should stop guessing.

## Risks

Render time is measured in the browser and will vary with the viewer's machine, which makes the distribution hard to act on and easy to dismiss. Reporting it separately from server-side time keeps the actionable part clean.

## Measurement

Dashboards with complete timing data, the share of total time attributable to each stage, and after the follow-on work, the ninety-fifth percentile against target.

## Prior Art

The two wrong guesses are the useful history. The first blamed chart rendering and produced a canvas rewrite that moved the median by under half a second. The second blamed payload size and added compression, which helped the largest dashboards and left the ninety-fifth percentile where it was. Both were reasonable readings of the single number available at the time. That is the case for instrumenting before touching anything, and it is the answer to give when someone asks why this phase ships no improvement.

## Dependencies

- A timing identifier that survives from the browser request down to each individual query, which the query layer does not propagate today
- Agreement on what useful means, since first paint, last chart, and first interactive produce three different medians
- Reporting that works for a dashboard author who cannot read a trace, which is a different artifact from the one the platform team would build for itself

## Open Questions

Whether attributing total time to the slowest query holds up when a dashboard fires twelve queries in parallel against the same warehouse and they contend with one another; the slowest may be slow because of the other eleven. Also unresolved: whether render time measured on the viewer's machine belongs in the author's view at all, given it is the number an author can least affect and the one most likely to be used to dismiss the rest.
