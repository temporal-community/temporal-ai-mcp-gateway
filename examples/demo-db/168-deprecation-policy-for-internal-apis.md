---
Name: Deprecation Policy for Internal APIs
Owner: Clara Benton
Status: Draft
Last Updated: 2026-07-25
---

## Context

Internal interfaces are changed by whoever owns them, sometimes with notice and sometimes not. The resulting breakages are absorbed as ordinary friction, which means the cost is real and invisible. Two teams have told us they maintain compatibility shims for interfaces that were changed without warning.

## Proposal

A written policy with notice periods proportional to the number of consumers.

- Consumers identified from the dependency map rather than from memory
- Notice periods tiered: two weeks for one consumer, a quarter for many
- Deprecation announced in a single channel teams can rely on, with the removal date stated
- Removal blocked while any consumer still calls, which is now measurable

## Scope

Service-to-service interfaces on the shared platform. Library interfaces within a repository are a different problem.

## Risks

A policy that blocks removal while any consumer calls gives every consumer a veto, including those who have had a quarter to migrate and have not. A deadline with an escalation path is necessary, and the escalation has to be used occasionally or the deadline is advisory.

## Measurement

Deprecations announced through the policy, breakages reported from unannounced change, compatibility shims maintained, and the average time from announcement to last call.

## Migration

The two known compatibility shims are the first test of the policy and the awkward case: the breaking change already happened, so there is nothing left to give notice about. Both get a removal date set by the owning team under the same tiering, which means the policy starts by imposing work on the teams that absorbed the breakage. That is still the right order, because a shim with no date on it is permanent.

- Existing shims inventoried from the two reports plus a sweep of the dependency map
- Each given a removal date and an owner before the policy is announced
- Single-consumer interfaces migrated first, where two weeks is enough

## Cost

The dependency map is the expensive part, not the policy. It is built from call traces sampled hourly, so a consumer calling once a month may never appear, and the removal block is only as good as that map. Holding a full quarter of traces is what makes a claim that no consumer still calls defensible, and that is storage on the tracing system that nobody has budgeted.

## Open Questions

The escalation path has no named escalation point. A deadline only the platform team can enforce makes that team the arbiter in every disagreement between two product teams, which they have not agreed to be. Whether this belongs with engineering leadership or with an architecture review group is unresolved, and the policy should not be announced before it is settled.
