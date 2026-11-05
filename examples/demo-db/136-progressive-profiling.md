---
Name: Progressive Profiling
Owner: Hana Kobayashi
Status: Draft
Last Updated: 2026-01-03
---

## Background

Signup collects what marketing needs for segmentation, which makes the form longer than it should be. Removing fields from signup, as proposed elsewhere, leaves a gap that someone needs to fill if segmentation is to keep working.

## Proposal

Collect the deferred attributes gradually, at moments where the question makes sense.

- Role asked when the person first does something role-specific, in context
- Team size inferred from workspace membership rather than asked at all
- Industry asked once, in settings, with a visible reason for why we want it
- Every question skippable without consequence and never repeated after a skip

## Scope

The three attributes currently collected at signup and genuinely used.

## Risks

Contextual questions interrupt a task the person chose to do, which is a worse moment than a form they expected. If the interruption cost exceeds the segmentation value, the right answer is to stop collecting the attribute rather than to find a better moment for it.

## Measurement

Collection rate per attribute against the signup-form baseline, skip rate, and task completion on the screens where questions appear.

## Sequencing

Team size goes first, because inferring it from workspace membership is not a question at all: it removes a field and adds no interruption anywhere, and it can ship before the signup change does. Industry second, in settings, where nobody is mid-task. Role last, since the contextual prompt is the only genuinely new pattern here and it should be built after the other two have settled what skip and never-ask-again actually do.

## Data We Have

The signup form currently returns role for about ninety percent of new accounts because the field is required, and that is the number every contextual version will be compared against. It is also an inflated number: a required dropdown answered to get past a form is not the same answer as one given in context, and nothing today tells us how often the stored value is simply the first option in the list. Marketing uses role across most segments, industry in a few, and team size in one campaign. That distribution should decide how much interruption each attribute is worth.

## Alternatives Considered

- Enrichment from the email domain and public sources, rejected on privacy grounds and because it is wrong often enough for small organizations to be worse than a blank
- Keeping role on the signup form and deferring only the other two, which is the smallest change and leaves the longest form in place at the point of highest drop-off
- A post-signup wizard asking all three, which is the same form wearing a different hat
