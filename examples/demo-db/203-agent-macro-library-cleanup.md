---
Name: Agent Macro Library Cleanup
Owner: Dmitri Volkov
Status: Draft
Last Updated: 2026-02-06
---

## Context

The macro library has four hundred and ten entries, accumulated over five years. Many describe product behavior that has since changed, several contradict each other, and the search within the library is poor enough that people recreate macros rather than find them.

## Proposal

Audit, consolidate, and put the library under ownership.

- Usage data pulled for every macro, with anything unused in six months removed
- Surviving macros reviewed for accuracy against current product behavior
- Consolidation of near-duplicates, which is roughly a third of the library
- A named owner per topic area, responsible for accuracy, with a quarterly review

## Non-goals

No change to the tooling. The library feature is adequate; its contents are the problem.

## Risks

Removing a macro that someone relies on produces an immediately worse experience for whoever used it, and usage data is a poor guide for seasonal cases such as renewal season or tax documentation. A two-week archive before deletion covers most of this, and the quarterly review is what keeps the remaining set honest.

## Measurement

Library size, share of responses using a library macro rather than free text, accuracy findings per quarterly review, and time to find a macro, measured by observation rather than by survey.

## Sequencing

Usage data first, consolidation last. Pulling six months of usage across four hundred and ten entries is a day of work and settles the argument about which ones matter. Reviewing accuracy before that means reviewing entries about to be archived. Consolidation goes last because merging near-duplicates is only safe once both have been checked against current behavior; merging two stale entries produces one stale entry with more readers.

- Usage pulled, unused set archived, archive visible to support staff
- Surviving entries reviewed for accuracy, one topic area at a time
- Near-duplicates merged after that review, never before

## Staffing

The accuracy review cannot be done centrally. It needs someone who knows how the area an entry describes behaves today. Four topic owners at roughly two days each covers the first pass. The quarterly review afterwards is an hour per owner if the library stays near its reduced size, and a second cleanup project if it does not, which is the argument for naming owners now rather than once the audit is over.

## Rollback

Archived entries are restorable individually for the full two weeks, by whoever misses one rather than through a request. That covers removal and nothing else. A consolidation cannot be undone the same way, because the merged entry has been edited since and restoring the originals restores text already judged inaccurate. Consolidations are reviewed by the topic owner before they take effect.
