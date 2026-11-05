---
Name: Internal Wiki Retirement
Owner: Caleb Mortensen
Status: Draft
Last Updated: 2025-09-22
---

## Context

We have two internal documentation systems: the old wiki and the current workspace. The wiki is read-only in practice but still receives traffic, mostly from search results, and a meaningful share of that traffic lands on pages that contradict current practice.

## Proposal

Migrate what is live, archive the rest, and turn the wiki off on a date.

- Traffic analysis to identify pages with genuine readership, which is a small minority
- Those pages reviewed and migrated by their owning team, not by a central effort
- Everything else exported to an archive that is searchable but clearly marked historical
- A shutdown date announced, with redirects to the archive

## Non-goals

No attempt to improve the content during migration, which would stall it.

## Risks

The pages nobody reads include a few that are read once a year by one person doing something critical, such as a yearly compliance filing. The announcement period needs to span at least two quarters, and the archive must stay searchable rather than being a storage bucket.

## Measurement

Pages migrated against pages archived, wiki traffic through the announcement period, archive searches after shutdown, and requests to restore a page.

## Sequencing

The traffic analysis comes first and sets everything else, because the migration list is an output of it rather than an input. Redirects go in before the announcement, so a reader following a stale search result lands on the archive instead of a dead page while the announcement is still fresh. The shutdown date is set only after every owning team has acknowledged its migration list; a date announced against an unacknowledged list moves, and a date that moves is not a date.

## Staffing

Migration work sits with owning teams, which spreads the cost but ties the schedule to their quarters.

- One coordinator for the traffic analysis, the redirect map, and the announcement
- A named owner per migrating page, drawn from the team that owns the subject
- Archive export and its search index built once, by the workspace team

## What Would Change Our Mind

If the traffic analysis shows readership is not a small minority but a long tail spread thinly across hundreds of pages, the per-team migration model collapses, and either the date moves out or the archive inherits far more than planned. The other signal is the restore request rate during the announcement period. Steady requests mean the archive is not serving the once-a-year reader, and we would keep the wiki readable past the shutdown date rather than claim the archive covers a case it does not.
