---
Name: Preview Environments per Branch
Owner: Erin Vasquez
Status: In Review
Last Updated: 2026-06-02
---

## Context

Reviewing a user-facing change means reading the diff and imagining the result, or checking out the branch and running it locally, which for front-end changes takes longer than the review. Design and product review therefore happens after merge, on staging, where changes are harder to undo.

## Proposal

An ephemeral environment per change, linked from the change itself.

- Created on first push, updated on each subsequent push, destroyed on merge or close
- Seeded with the standard sample dataset rather than with production data
- Linked automatically in the change description
- A lifetime cap, since abandoned branches would otherwise accumulate environments

## Scope

The web product. Mobile preview needs a different mechanism and is not covered here.

## Risks

Environments that look real invite testing against them as if they were, including by people outside engineering who may not realize the data is synthetic. Clear visual marking and a banner are the minimum, and the sample dataset must never be seeded from production, however convenient that would be.

## Measurement

Changes with a working preview, design and product review happening before merge rather than after, and infrastructure cost of the environment pool.

## Cost

The pool scales with open changes rather than with engineers. We hold about forty open changes against the web product at any time, and each preview keeps a web process, a database, and the seeded data alive while the change stays open.

- Idle environments suspended after four hours without a request and restored on the next one, trading a slow first load for most of the saving
- A fourteen-day lifetime cap, which covers the long tail of open changes without keeping abandoned ones alive
- Seeding from the sample dataset rather than a snapshot, so storage per preview is small and identical

## Dependencies

The standard sample dataset has to be good enough to exercise the surfaces under review, and today it is not: it has no multi-workspace accounts and no long listing histories, which are two of the places front-end changes most often break. Extending the seed is a prerequisite rather than a follow-up. The change system also has to keep the link correct across a force-push, and a rebase must not rebuild the environment from scratch, or reviewers stop trusting that the link shows the current state.

## Open Questions

- Whether people outside engineering get links directly or only through the reviewer who asked for a look
- Whether a preview survives briefly after merge, since the question of what it looked like usually arrives once it is gone
- What happens to a change that needs a feature flag enabled, which is a staging-only operation today
