---
Name: Test Data Generation for Pipelines
Owner: Ben Tsai
Status: Draft
Last Updated: 2025-12-05
---

## Background

Pipeline tests run against fixtures copied from production two years ago and trimmed by hand. They do not contain any of the shapes that have caused the last ten incidents, because those shapes did not exist when the fixtures were made.

## Proposal

Generate test data from the live schema with properties drawn from production distributions, without copying production rows.

- Generators derived from the registered schema, so they stay current automatically
- Distributions sampled from production aggregates rather than from rows
- Edge cases from past incidents captured as named scenarios and kept in the suite
- Deterministic seeding, so a failing test is reproducible

## Scope

Transformation tests. Integration tests against operational systems are a separate problem with a different constraint.

## Risks

Generated data is a model of production, and models are wrong in the direction of the modeler's assumptions. The named-scenario library is what keeps the suite honest, and it only grows if adding a scenario after an incident is part of the incident process rather than an afterthought.

## Measurement

Fixture age, coverage of the named scenario library, and the share of incidents whose shape was reproducible in a test before the fix.

## Migration

The two-year-old fixtures do not get deleted on the day the generators land. They get pinned as one more named scenario, because whatever they contain is the only record of shapes the schema no longer describes, and some transformations still have branches that only those rows reach. Suites convert one at a time, and a suite is converted when its assertions pass against generated data without being relaxed. A test that needs its expectations loosened to accept generated input is reporting a modeling gap, not a flaky fixture.

## Review Notes

- Sampling from aggregates rather than rows is the load-bearing choice, and it is what keeps this out of the privacy review that copying production would require
- Determinism needs to hold across generator versions, or a seed recorded in an incident writeup stops reproducing anything a quarter later
- The named scenarios from the last ten incidents should be written before the generators, since they are the acceptance criteria
- Nothing here helps a transformation whose bug is in its handling of volume rather than shape

## Rollback

Reverting is cheap while the old fixtures are still pinned, and that is the reason to keep them rather than a sentiment about them. If generated data produces failures nobody can attribute, a suite goes back to its fixture with the generator left running alongside in a reporting-only mode. Removing the old fixtures is a separate decision, made per suite, after a quarter of the generated version holding up.
