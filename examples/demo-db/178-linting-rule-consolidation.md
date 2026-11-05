---
Name: Linting Rule Consolidation
Owner: Dana Whitfield
Status: Draft
Last Updated: 2026-01-09
---

## Background

Each repository has its own lint configuration, accumulated independently. Some rules contradict each other across repositories, so moving between them means fighting the formatter. A meaningful share of review comments are about style that a tool should settle.

## Proposal

One shared configuration, adopted repository by repository, with formatting fully automatic.

- A single base configuration owned by the platform team, with documented deviation points
- Formatting applied on commit rather than checked in review
- Rules split into errors and warnings, with warnings not blocking
- A one-time reformatting commit per repository, excluded from blame

## Non-goals

No new rules in the first pass. Consolidating what exists is enough change at once.

## Risks

The reformatting commit touches every file and makes history harder to read, which is a real and permanent cost paid for a recurring benefit. Excluding it from blame mitigates the common case but not every tool respects that.

## Measurement

Repositories on the shared configuration, style-related review comments, and time spent on formatting failures in continuous integration.

## Migration

Repository order matters more than speed. The first two should be repositories with few long-lived branches, since every one of those turns the reformatting commit into a conflict in every file it touches.

- Open branches rebased or merged before the reformat lands, announced a week ahead
- The blame ignore file added in the same commit, so no window exists where history reads badly
- Deviation points recorded in the repository rather than in the platform team's memory

## Failure Modes

A repository adopts the base configuration and then quietly accumulates local overrides, which is how the current state was reached. Formatting on commit fails silently for anyone whose hook is not installed, so the continuous integration check becomes the real gate again. And a rule promoted from warning to error later lands on every repository at once unless promotion is decided per repository.

## What Would Change Our Mind

If style-related review comments do not fall after the first three repositories, those comments are not about rules a tool can settle, and this is a formatting convenience rather than a review one. That would not stop the work, and it would change the argument for it, which currently rests on review time.
