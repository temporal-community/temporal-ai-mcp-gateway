---
Name: Service Dependency Map
Owner: Lena Fischer
Status: Draft
Last Updated: 2025-11-02
---

## Background

We have a dependency diagram maintained by hand in a drawing tool. It was last updated eleven months ago, it omits at least four services that have been created since, and during the last incident nobody opened it.

## Proposal

Derive the map from observed traffic and from declared dependencies, and reconcile the two.

- Observed edges from service mesh telemetry, refreshed continuously
- Declared edges from each service's own manifest, maintained by its team
- Discrepancies between observed and declared surfaced as a report, since each direction means something different
- The map queryable rather than only viewable, so tooling can use it

## Scope

Services on the shared platform. The two services outside it should either be onboarded or declared as external dependencies.

## Risks

An undeclared but observed dependency is usually a shortcut someone took under pressure, and surfacing it will be read as criticism. The report needs to be framed as finding gaps in the declaration rather than finding fault, or teams will start routing calls to avoid detection.

## Measurement

Services with a current manifest, discrepancies between observed and declared, and whether the map is opened during the next three incidents.

## Sequencing

Observed edges ship first, alone, with no declaration requirement and no discrepancy report. A map that is merely current already beats the drawing tool, and it can be in front of on-call within about three weeks. Manifests follow. Asking teams to declare before they can see what the mesh shows invites them to copy the observed list and submit it as a declaration, which produces a reconciliation that always agrees and proves nothing.

## Interfaces Affected

- A query endpoint over the map, wanted by both incident tooling and deploy checks, which fixes the data shape earlier than is comfortable
- The service manifest, which gains a dependencies block and therefore a schema version
- The incident channel template, where the useful artifact is one service's blast radius rather than the whole graph
- The hand-drawn diagram, which should be deleted rather than left to contradict the map

## Failure Modes

Mesh telemetry sees only what crosses the mesh. Direct datastore access, queue consumption, and anything reached through a shared library's connection pool are invisible to it, and those are the edges that hurt during an incident. A map that is confident about request traffic and silent about the queue is worse than the stale diagram, because the stale diagram was not trusted. Every edge should carry how it was observed, and the absence of queue edges belongs on the map itself rather than in a note somewhere else.
