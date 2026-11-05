---
Name: Writing Style Guide Adoption
Owner: Maya Brennan
Status: Draft
Last Updated: 2026-07-31
---

## Context

We have a style guide. It is a wiki page, last updated two years ago, that most people writing product text have not read. Product copy, documentation, and support macros each have their own conventions, and customers encounter all three.

## Proposal

Make the guide usable where writing happens rather than where it is stored.

- The guide rewritten as rules with examples, not principles with aspirations
- Automated checks for the mechanical rules in documentation and product copy
- A short reference card for the dozen rules that cover most of the variation
- Ownership assigned, with a quarterly review rather than ad hoc edits

## Non-goals

No enforcement on internal writing, which has a different audience and should not be policed.

## Risks

Automated checks catch mechanical consistency and miss everything that matters about writing, and a product whose copy passes every check can still be unclear. The checks should be framed as the floor rather than the standard, or people will write to them.

## Measurement

Check pass rate on new copy, variation in the dozen target rules across surfaces, and whether support macros and documentation converge on the same terminology.

## Prior Art

The documentation team has run mechanical checks for a year, and their experience is why these are framed as a floor: pass rates reached ninety percent within two months and the writing did not measurably improve, because the automatable rules were the ones nobody was getting wrong. What did change was terminology drift, which the checks caught reliably and which is also what customers notice across surfaces.

## Interfaces Affected

- The documentation build, which already runs a checker and gains the new rule set
- The product copy pipeline, where strings live in the repository and can be checked in the same pass as code
- Support macros, edited in the support console, with no checking surface at all
- The reference card, which has to live where people write rather than in the wiki page that failed

Macros are the awkward case. Checking them means either a check inside the console or an export reviewed on a schedule, and the export is what we can actually have this quarter.

## Staffing

An owner who can decide is the whole proposal. The rewrite is about three weeks for a writer and the quarterly review is a day. Without a named owner the guide returns to the state it is in now, which is the thing this page exists to fix rather than a risk to be managed around.
