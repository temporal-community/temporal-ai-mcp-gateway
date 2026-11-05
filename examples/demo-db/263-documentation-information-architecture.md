---
Name: Documentation Information Architecture
Owner: Nikhil Shah
Status: In Review
Last Updated: 2026-04-15
---

## Problem

The documentation is organized by product area, which matches our team structure and not the questions people arrive with. Search carries most of the traffic, navigation carries almost none, and the pages people land on frequently assume context they have not been given.

## Proposal

Restructure around tasks, with reference material separated from guidance.

- A task-based top level derived from the actual entry queries, not from the product map
- Reference material separated clearly, since it is read differently and maintained differently
- Every page stating its assumptions and linking the prerequisite, rather than assuming
- Redirects from every existing path, since documentation links are everywhere

## Scope

The public product documentation. The developer interface reference has its own structure and audience.

## Risks

Restructuring breaks the mental model of people who know the current layout, who are disproportionately our support team and our most engaged customers. Redirects handle the links; they do not handle the habit, and the complaint will be loud and from people whose opinion we value.

## Measurement

Navigation use against search use, task completion in testing, support tickets citing documentation confusion, and landing page bounce rate.

## Sequencing

Derive the task taxonomy from entry queries and publish it for comment before a single page moves. The taxonomy is cheap to argue about and expensive to redo, and the support team belongs in that argument early rather than meeting its conclusion. Reference material moves second, because that is a relabel rather than a rewrite. Guidance pages move last and one task cluster at a time, each cluster going live with its redirects on the same day.

## Staffing

The bulk of this is not writing. Deriving the taxonomy is research, the moves are mechanical, and stating assumptions with a link to the prerequisite is effectively a pass over every guidance page, which is the long pole by a wide margin. Two writers for a quarter covers the taxonomy and the moves. The prerequisite work is open-ended and should be scoped cluster by cluster rather than estimated as one number that will be wrong.

## Rollback

Reverting a cluster means reversing its redirects, which stays possible only while the old paths remain unused, so the standing rule is that a retired path is never recycled for new content. What cannot be rolled back is habit: a cluster reverted after two weeks leaves the people who adapted fastest, mostly support and the most engaged customers, wrong twice. That argues for deciding a cluster is final before it ships rather than treating the first weeks as reversible.
