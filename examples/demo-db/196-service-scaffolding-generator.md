---
Name: Service Scaffolding Generator
Owner: Marcus Reyes
Status: Approved
Last Updated: 2026-06-13
---

## Context

Creating a new service means copying an existing one and deleting what you do not need. The copied service brings its original's dependencies, its outdated configuration, and occasionally its bugs. Three services currently carry a logging configuration that was wrong when it was copied two years ago.

## Proposal

A generator producing a correct, minimal service with the platform integrations wired.

- One command producing a service with health checks, metrics, tracing, and deployment definitions
- Platform integrations current by construction, since the template is maintained
- Generated services registered in the ownership directory automatically
- A migration path for existing services to adopt template updates

## Scope

Services on the shared platform in the two supported languages.

## Risks

A template is only correct at generation time, and generated services drift from it immediately. The migration path is what keeps the fleet coherent, and it is the part that generators usually lack. Without it this improves the first day and nothing afterwards.

## Measurement

New services created from the template, time from decision to a deployed skeleton, and the spread of platform integration versions across the fleet.

## Staffing

A template is a product with users, and an unowned template is a copied service with extra steps.

- One owner per language, since the two templates will diverge in structure and only the platform integrations need to stay aligned
- Template changes reviewed by the platform teams whose integrations they wire, not by the template owner alone
- A rotation for the migration pull requests, which is where the ongoing cost sits rather than in the generator

## Failure Modes

A generated service edited past the point where template updates apply cleanly, which happens to every service eventually and is why the migration path has to tolerate divergence rather than assume it away. A template update that is correct in general and breaks a service whose traffic pattern the template never anticipated. And automatic directory registration recording the generating engineer's team, which is right on the day and wrong after the first reorganization.

## Open Questions

Whether migration pull requests are opened automatically or offered, where opening them keeps the fleet coherent and fills queues with changes nobody asked for. The three services carrying the inherited logging configuration are the test case: they were never generated from a template, so adopting updates means adopting the template first, and nothing here says who does that work or when.
