---
Name: Localization Quality Review
Owner: Ruth Adeyemi
Status: In Review
Last Updated: 2026-02-08
---

## Problem

Translations are delivered by a vendor, imported, and never reviewed by anyone who speaks the language and uses the product. We have found, through customer reports, translated strings that were grammatically correct and completely wrong in context, including a confirmation button that said the opposite of its action.

## Proposal

In-context review before release, by people who use the product.

- Screenshots or a preview build provided to reviewers with the strings in place
- Reviewers recruited from customer-facing staff who speak the language, paid for the time
- A glossary of product terms maintained and provided to the vendor, which does not currently exist
- Strings with missing context flagged by the vendor rather than guessed at

## Scope

The eleven supported languages, with review depth weighted by user population.

## Risks

In-context review is slow and will delay releases in the languages reviewed, and the people best placed to review have other jobs. Scoping review to new and changed strings rather than the whole corpus keeps this feasible; reviewing everything would be a project rather than a process.

## Measurement

Strings reviewed in context before release, context-error findings, translation-related support tickets, and release delay attributable to review.

## Staffing

Scoped to new and changed strings, review comes to roughly two hours per language per release cycle, more for the three languages whose surfaces change most. That is twenty-odd hours a cycle taken from people whose main job is customer-facing. It needs to be paid time agreed with their manager rather than a favor, or it becomes the first thing dropped in a busy week and the review turns into a signature. Two of the eleven languages have exactly one plausible reviewer in the company, which is a single point of failure worth naming before it is tested.

## Dependencies

- A preview build per language that a non-engineer can open without a development environment
- String extraction that carries the screen a string appears on, which the current pipeline discards
- The glossary, which has to exist before the vendor can be held to it and which nobody owns today
- A path for reviewer findings back into the vendor's workflow instead of a spreadsheet someone mails around

## Operational Impact

Release becomes conditional on review in the reviewed languages, so the release manager needs a per-language view of review state and a written rule for shipping without it. The vendor relationship changes too: asking them to flag missing context rather than guess is a contract change and probably a price change, and it moves effort from their guesswork to our context-writing. Whoever writes that context is not currently anyone, and that gap will decide whether this holds up after the first quarter.
