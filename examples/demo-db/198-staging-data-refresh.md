---
Name: Staging Data Refresh
Owner: Caleb Mortensen
Status: Draft
Last Updated: 2026-02-17
---

## Context

Staging data was seeded two years ago and has drifted into a state that resembles nothing. Testing against it produces false confidence: the shapes that break in production, such as accounts with thousands of members or workspaces with deeply nested content, do not exist in staging.

## Proposal

Refresh staging regularly from production shapes without copying production data.

- A generator producing data matching production distributions, including the extreme shapes
- Weekly refresh, replacing rather than accumulating
- A stable subset that does not change between refreshes, for tests that need fixed fixtures
- No production rows, ever, which is both a privacy requirement and a discipline

## Scope

The staging environment. Preview environments use the same generated dataset.

## Risks

Generated data misses the shapes nobody thought to generate, which includes the ones that cause incidents. The generator should be fed by production aggregate statistics rather than by imagination, and every production incident caused by a data shape should add a case to it.

## Measurement

Defects found in staging that would previously have reached production, staging data age, and the number of production incidents attributable to a data shape absent from staging.

## Operational Impact

A weekly replace is a scheduled destruction of whatever anyone left in staging, and that has to be understood rather than discovered.

- The refresh window is published and fixed, so manual test setup is never more than a week of work to lose
- The stable subset is the only promise; anything outside it is gone on refresh day
- A failed refresh leaves last week's data rather than an empty environment, since empty is worse than stale
- Preview environments take the dataset at creation, so a long-lived preview drifts from staging by design

## Cost

The generator is the build. The recurring cost is the statistics feed and keeping case coverage current. Every schema change has to update the generator in the same change, or the refresh produces data the application no longer understands and staging is useless in a new way. That coupling is the real ongoing price, and it is still cheaper than maintaining a sanitized copy of production.

## Open Questions

How the stable subset stays stable across a schema change, since it has to be regenerated and the fixtures that depend on it expect particular identifiers. The other is where the production distributions come from and how often they are recomputed, because reading them is itself an access question, and monthly statistics may be enough underneath a weekly data refresh.
