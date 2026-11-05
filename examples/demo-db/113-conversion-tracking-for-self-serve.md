---
Name: Conversion Tracking for Self-Serve
Owner: Amara Osei
Status: Draft
Last Updated: 2025-11-23
---

## Context

We cannot connect a signup to what preceded it. Marketing reports channel performance from their own tooling, product reports signups, and the two sets of numbers have never agreed. The discrepancy is currently about eleven percent and nobody can explain it.

## Proposal

One identity thread from first touch to paid conversion, owned by the data team.

- A first-party identifier set on first visit and carried through signup
- Server-side event recording, not dependent on client tooling that ad blockers remove
- A documented reconciliation between marketing tooling and product data, run monthly
- Attribution computed in one place and consumed by both teams

## Scope

Self-serve acquisition. Enterprise pipeline attribution is a sales operations problem with different mechanics.

## Risks

First-party identifiers carried across a signup boundary are personal data from the moment they are joined to an account, and the retention and consent treatment needs to be settled before the implementation, not retrofitted to it.

## Measurement

Discrepancy between marketing and product signup counts, share of signups with a resolved first touch, and whether channel budget decisions begin using the shared numbers.

## Interfaces Affected

The identifier has to be set before anything else happens on a first visit, which puts it in the edge layer rather than in the application, and it has to survive the move from the marketing site to the product, which are separate origins today. Signup gains the join between identifier and account, and that join is the moment the data becomes personal. Marketing tooling keeps its own collection, since the reconciliation reads both rather than replacing one, and that is what makes the eleven percent explainable instead of absorbed.

## Sequencing

Consent and retention treatment are settled first and in writing, because they govern where the identifier may be stored and for how long, and retrofitting that is the failure the risks section names. Server-side recording follows and runs alongside the existing collection for a month, which is how the discrepancy gets attributed rather than merely reduced. Shared attribution comes last, after both teams have read the same numbers for a full reporting cycle.

## Open Questions

What the identifier does when consent is refused, since that visitor still signs up and still has to be counted somewhere, and leaving them out of attribution creates a discrepancy in the other direction. We have also not agreed who arbitrates when the reconciliation finds a gap neither tool can explain, which on current evidence happens in the first month.
