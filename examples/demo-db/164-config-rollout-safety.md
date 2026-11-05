---
Name: Config Rollout Safety
Owner: Erin Vasquez
Status: Approved
Last Updated: 2026-02-07
---

## Problem

Configuration changes deploy globally in one step. Two of our last five significant incidents were configuration changes that were correct in staging and wrong in production, and in both cases the whole fleet had the bad value within thirty seconds.

## Proposal

Treat configuration like code: staged rollout, automatic verification, fast rollback.

- Changes applied to one percent of instances, then ten, then the fleet, with pauses
- Health verification between stages, with automatic halt on regression
- Rollback to the previous value as a single action, available for seven days
- A diff and an approval for changes to the designated critical keys

## Scope

Runtime configuration served by the configuration service. Secrets and infrastructure definitions follow different paths.

## Risks

Staged rollout means a period where instances disagree about configuration, which for some keys is harmless and for others produces inconsistent behavior that is worse than either value. Keys that cannot tolerate disagreement need marking, and that marking depends on service owners knowing which of theirs those are.

## Measurement

Incidents attributed to configuration change, time to rollback, and the share of changes going through staged rollout rather than an emergency path.

## Sequencing

Rollback ships first and alone. One action that restores the previous value, available for seven days, would have shortened both of the incidents behind this document, and it needs none of the staging machinery to work. Staged rollout second. Key marking third, deliberately, because service owners answer the question of which keys tolerate disagreement far better after they have watched a staged rollout than before they have seen one.

## Failure Modes

- An emergency path quicker than the staged path, which becomes the normal path within a month unless every use of it is visible and reviewed
- Health verification keyed to lagging metrics, so a change that breaks an hourly job looks healthy at every stage and is fleet-wide before it shows
- A first stage that is not representative, all in one region or all on the oldest hosts, making one percent a weaker signal than it looks
- Rollback to a previous value that is no longer valid because a different key moved underneath it

## Open Questions

How long the pauses between stages should be, which is really a question about how fast a bad value becomes visible. The two incidents cited took very different times to surface, and the slower one argues for a pause nobody will accept on a routine change. Also unsettled: whether a key marked as intolerant of disagreement should be barred from staged rollout altogether, or pushed fleet-wide with the approval gate as its only protection, which is what we do today for everything.
