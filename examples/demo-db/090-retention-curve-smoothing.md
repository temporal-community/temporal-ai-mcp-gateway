---
Name: Retention Curve Smoothing
Owner: Grace Lindqvist
Status: Draft
Last Updated: 2025-09-04
---

## Problem

Retention curves for small cohorts are visually dominated by noise. A cohort of forty accounts produces a jagged line that people read as a weekly pattern, and we have seen roadmap discussions anchored on bumps that were four accounts.

## Proposal

Show uncertainty rather than hiding it, and smooth only with the raw data still visible.

- Confidence bands rendered by default on any curve below a sample threshold
- Optional smoothing with the raw points retained underneath, never replacing them
- A sample size indicator per point, not just per cohort
- A warning when a cohort is too small for the chart to carry meaning

## Non-goals

No change to how retention is computed, which is a separate piece of work in the cohort reporting proposal.

## Risks

Smoothing is a visual claim about the underlying process and will be read as the truth rather than as a rendering choice. Keeping the raw points visible is what prevents that, and it should not be configurable away for the sake of a cleaner slide.

## Measurement

Charts rendered with bands, decisions referencing small-cohort movements, and whether the warning changes what people say in reviews.

## Prior Art

The experiment readout tooling settled the same argument two years ago by refusing to show a result without its interval, and the objection then was the one we will hear now: the charts look busier and the slides look less certain. It faded within a quarter, and that reporting is the only place where someone can point at a number and say what it does not support. The difference here is that retention curves are exported into decks far more often, so the band has to survive the export rather than live in the tool.

## Interfaces Affected

Every surface that draws a retention curve, which is more of them than the chart library suggests.

- The cohort explorer, where bands and a per-point sample size both fit comfortably
- Scheduled report images, rendered with no viewer and no tooltip to carry sample size
- Slide exports, where a band drawn as a faint shade disappears on a projector

## Review Notes

Analytics accepted default-on bands and pushed back on the warning, arguing that a chart carrying a warning stops being used rather than being used carefully. The counter is that the four-account bump has already redirected a roadmap conversation, and a chart nobody opens does less damage than one read with confidence. The sample threshold was left to analytics, since it is a judgment about our cohort sizes rather than a general rule.
