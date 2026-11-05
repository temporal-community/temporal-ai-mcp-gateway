---
Name: Metric Definition Change Log
Owner: Nora Sellers
Status: Shipped
Last Updated: 2025-06-11
---

## Problem

Metric definitions changed without record. A number would shift between quarters and nobody could say whether the business moved or the definition did, which made historical comparison a matter of belief rather than evidence.

## Approach

A change log attached to every defined metric, written at the time of change and visible wherever the metric appears.

- Every definition change recorded with date, author, reason, and the expected effect
- Charts annotated at the date of change, so the step is explained where it appears
- Historical values retained under the old definition rather than restated
- A quarterly summary of definition changes circulated with the business review

## Non-goals

No approval workflow. The goal was record, not control, and adding approval would have slowed legitimate corrections.

## Risks

The discipline risk was that people would change definitions without logging them. Making the log the mechanism of change rather than a document about the change was what made this stick: the definition cannot be edited except through the logged path.

## Outcome

Shipped in May. Eleven definition changes have been logged since, three of which explained chart steps that would otherwise have been investigated as business events.

## Interfaces Affected

A log is only useful where the number is read, so every surface that renders a defined metric had to move.

- The chart library, which gained an annotation layer keyed to change dates rather than a hand-maintained list
- The metric catalogue, where the log renders in full beneath the definition
- Scheduled exports, which now carry a definition version beside each value, so a spreadsheet built last quarter can be identified as built on an old definition
- The business review deck, which pulls the quarterly summary rather than relying on someone to mention it

## Prior Art

Warehouse schema migrations have carried a change log for years and nobody reads it, which was the warning. The difference is placement: the schema log lives beside the schema, while this one renders on the chart where the step appears. Three of the eleven entries did their work because somebody met them while asking why a line jumped, not because anyone went looking.

## Open Questions

- Whether an upstream source change that moves a metric without touching its definition belongs in the same log, since the reader cannot tell the two apart from the chart
- Whether retaining history under an old definition should ever be revisited when that definition was simply wrong
- What the log does for a deleted metric, given the charts referencing it survive in old decks
