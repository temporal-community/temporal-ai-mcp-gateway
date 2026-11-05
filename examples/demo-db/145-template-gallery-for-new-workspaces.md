---
Name: Template Gallery for New Workspaces
Owner: Yusuf Demir
Status: In Review
Last Updated: 2026-06-21
---

## Problem

A new workspace is empty. The blank state is the single largest drop-off point in onboarding, and interviews consistently describe the same experience: people know what they want to do and cannot see how this product does it.

## Proposal

A gallery of starting templates, surfaced at creation and suggested by context.

- Twenty templates covering the common use cases, authored rather than crowd-sourced
- An AI suggestion step that reads the workspace name and the signup answers and proposes three
- Templates applied with sample content that is obviously sample, and removable in one action
- Usage tracked per template so the set can be pruned rather than only added to

## Scope

New workspace creation. Adding a template to an existing workspace is a different interaction and comes later.

## Risks

Suggestion from a workspace name is a thin signal and will often be wrong, which is fine if the suggestions sit beside the full gallery and are not presented as a conclusion. It stops being fine if the gallery is collapsed behind the suggestions, which is the version that will test better on first click and worse on week-four retention.

## Measurement

Workspaces starting from a template, week-one activation for templated versus empty workspaces, and sample content removal rate, which tells us whether the templates fit.

## Staffing

Twenty authored templates is the expensive line, and it is not an engineering cost. Each needs someone who understands the use case to build it and to populate it with sample content that reads as real without being mistaken for real. Two months of a designer and a writer produces the first set; a quarter of a person indefinitely keeps it from rotting. A stale template is worse than none, because it teaches a pattern the product no longer supports.

- Design and writing for the initial twenty, roughly two months
- A standing owner for template accuracy, reviewed quarterly against usage
- Localization decided per template rather than for the whole set, since sample content does not translate mechanically

## Rollout

The gallery ships before the suggestion step. That order is what makes the suggestions measurable: with the gallery alone, the distribution of what people choose becomes the baseline that three suggestions either beat or do not. Shipping both at once leaves no way to attribute a week-one activation difference to either half.

## Operational Impact

Applying a template creates content on someone's behalf, which touches storage limits and audit logging on a workspace's first day. A template applied and then abandoned leaves a workspace that looks active in reporting and is not, so templated workspaces have to stay distinguishable in the activation numbers rather than counting as ordinary creations.
