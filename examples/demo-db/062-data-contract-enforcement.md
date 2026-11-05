---
Name: Data Contract Enforcement
Owner: Hugo Takahashi
Status: Draft
Last Updated: 2025-11-07
---

## Background

We have written data contracts for the six most important sources. They are documents. Nothing checks whether the data matches them, so three of the six have drifted, and we know this because an analyst noticed, not because anything alerted.

## Proposal

Make contracts executable and check them continuously against the data they describe.

- Contract expressed as a machine-readable specification alongside the prose
- Checked at ingest for structure and daily for the semantic clauses
- Violations routed to the producing team with the specific clause cited
- A visible contract status per source, green or not, in the catalog

## Scope

The six existing contracts, then any new source that reaches a defined importance threshold.

## Risks

Semantic clauses are the valuable ones and the hard ones to express. A contract that only checks structure gives false comfort, since structural drift is already caught by the schema registry. If we cannot express the semantic clauses for a source, that should be stated rather than quietly skipped.

## Measurement

Clauses expressed as checks against clauses written in prose, violations found before a consumer notices, and the number of sources with a green status.

## Rollout

Start with the two sources that have drifted and whose producing teams already own the ingest path. Structural checks go first because they can be generated from existing schema registry entries with no new prose. Semantic clauses follow one source at a time, written with the producing team rather than for them, since a clause nobody agreed to is a clause that gets muted. The catalog status stays hidden until all six sources carry at least one semantic clause; publishing a green badge that only reflects structure would repeat the false comfort the risks section warns about.

## Operational Impact

Daily semantic checks put a recurring triage load on producing teams that they do not carry today.

- Violations arrive with the clause text, the failing rows, and the run timestamp
- A violation not acknowledged within two business days escalates to the source owner
- Muting a clause requires a replacement clause or a dated exception

## Open Questions

Who holds the pen when a producing team disputes a semantic clause. The contract is a joint document, but the consuming side wrote most of the prose, and an unresolved dispute leaves a source in a non-green state nobody can clear. We also have not decided whether a violation should block the daily load or let it through annotated; blocking protects consumers and breaks dashboards, annotating does the reverse.
