---
Name: Chart Library Consolidation
Owner: Priya Raman
Status: Draft
Last Updated: 2026-01-05
---

## Problem

Three charting libraries are in use across the analytics product, the admin console, and the embedded reports. They disagree about color, about axis behavior, and about what a null value looks like, so the same data renders differently depending on where you see it.

## Proposal

Standardize on one library with a shared configuration layer.

- A single wrapper package owning theme, number formatting, and empty states
- Migration surface by surface, starting with the embedded reports, which are the most visible externally
- Accessibility checks applied in the wrapper rather than left to each chart
- The other two libraries removed from the dependency list rather than merely unused

## Scope

Charts in product surfaces. Internal notebooks and ad-hoc analysis are unaffected.

## Risks

Migration touches every chart, which is several hundred, and most of them are fine. The temptation will be to improve them while migrating, which turns a mechanical change into a design project and stalls it. The rule should be visual parity first, improvements afterwards and separately.

## Measurement

Charts migrated, libraries in the dependency list, and visual inconsistencies reported, which currently arrive at about one a week.

## Alternatives Considered

Writing the wrapper over all three libraries and leaving them in place would fix the visible inconsistency without a migration. It fails because the disagreements are not all configurable: null rendering and axis tick selection are decided inside two of the three and cannot be overridden from outside, so the wrapper would normalize color and formatting while leaving exactly what people report. Building our own charting layer on a drawing primitive was dismissed on cost; our charts are ordinary and nothing about them justifies owning that.

## Staffing

Several hundred mechanical changes belonging to no single team is how consolidations die. The wrapper needs one owner for its lifetime, and the migration should be distributed to the teams owning each surface.

- Wrapper owned by the design systems team, who already own the theme
- A lint rule blocking new charts on the old libraries from the day the wrapper exists
- Each surface tracked against a named owner and a date

## Rollback

Per-chart rollback is not worth building. A migrated chart that renders wrong gets fixed forward, since the old library stays in the dependency list until its surface is finished. The real rollback point is the library choice itself, and that has to be settled on the embedded reports before the other surfaces start.
