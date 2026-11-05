---
Name: PII Tagging and Masking
Owner: Caleb Mortensen
Status: In Review
Last Updated: 2026-03-16
---

## Context

Personal data is identified by column name convention, which works until someone names a column differently. Our last review found personal data in nine columns that no convention would have caught, including free-text fields where it arrived by accident.

## Proposal

Explicit tagging at the column level, with masking applied from the tag rather than from the name.

- Tags applied by the dataset owner and required for new columns
- A scanner that samples free-text columns and proposes tags for review
- Masking policies applied from tags at query time, varying by access tier
- Untagged new columns default to masked until classified

## Non-goals

No change to what we collect. This is about handling what we already have correctly.

## Risks

Defaulting new columns to masked will break pipelines that read them before anyone classifies them, which is deliberate friction but friction nonetheless. The classification step has to be fast and obvious or it becomes a reason to avoid adding columns, which has its own costs.

## Measurement

Columns tagged as a share of the total, personal data found in untagged columns during the next review, and pipeline breakages caused by the default, which should trend to zero as the habit forms.

## Migration

The columns we already have are the larger job and the one with no forcing function, since the default-to-masked rule only touches new ones.

- Convention-named columns get tags derived from the convention, reviewed in bulk by the dataset owner
- The nine columns from the last review are tagged by hand first, because they are the known misses
- Free-text columns wait for the scanner and keep their current visibility until then

Masking every untagged column on day one is the stricter choice and would break more pipelines in an afternoon than the tagging work saves in a quarter.

## Failure Modes

A tag applied to the right column in the wrong copy of a dataset, since several of these tables are replicated and the tag lives with the column definition. A scanner that samples a free-text column in a quiet week, sees nothing personal, and proposes a tag of none. And the quiet one: a masking policy enforced at query time but not on the export path, which is how the data leaves anyway.

## Open Questions

Who classifies a column when the dataset owner has left and the inheriting team does not know what the field holds. The default keeps it masked, which is safe and leaves a pipeline broken with nobody able to unbreak it. We have also not decided whether a scanner proposal expires, since a free-text column reviewed once can start receiving personal data a year later.
