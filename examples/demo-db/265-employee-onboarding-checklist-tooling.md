---
Name: Employee Onboarding Checklist Tooling
Owner: Jonas Keller
Status: Draft
Last Updated: 2025-12-20
---

## Context

New joiner onboarding is a document that the hiring manager copies and adapts. Steps are missed, particularly the ones owned by other teams, and the most common miss is equipment or access that should have been arranged before the start date.

## Proposal

A checklist generated from role and location, with steps assigned to their actual owners.

- Templates per role family and location, generated at offer acceptance
- Steps assigned to the owning team with due dates relative to the start date
- Visible status for the hiring manager without their having to chase
- Completion data feeding template improvement, since the same steps are missed repeatedly

## Scope

Pre-start and first-week onboarding. Role-specific training beyond the first week stays with teams.

## Risks

A checklist with steps owned by other teams only works if those teams see it in their own tools. A system that requires them to check a separate tool will be ignored, and the hiring manager will go back to chasing, which is the current state with extra overhead.

## Measurement

Steps completed before start date, equipment and access ready on day one, and new joiner survey responses on the first week.

## Interfaces Affected

Three systems, and one of them is not ours. Offer acceptance in the applicant tracking system is the trigger, so it needs an event we can read rather than a nightly export. Steps for the equipment and access teams land in the ticket queues they already work from, with the checklist holding a reference instead of its own copy of the state. The hiring manager's view reads status back from those queues; a step completed in the queue and not reflected sends the manager back to chasing, which is the one job this has.

## Rollout

One role family in one location first, chosen where the equipment team already works from a queue, since that is what the design assumes. Templates for other locations follow after four or five joiners have run through the first one, because location differences live in the detail of who provides what and are found by being wrong about them.

## Failure Modes

- A start date that moves after generation, leaving due dates anchored to the old one
- A role that fits no template, where the manager adapts the nearest one and the gap is invisible
- A step completed as a favor outside the queue, so the checklist shows red for something that is done
- An offer accepted and then withdrawn, with equipment already ordered
