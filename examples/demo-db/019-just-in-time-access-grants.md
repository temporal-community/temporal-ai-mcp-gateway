---
Name: Just-in-Time Access Grants
Owner: Omar Haddad
Status: Draft
Last Updated: 2025-12-19
---

## Background

Internal access to production data is granted permanently because requesting it is slow. The result is a long tail of people holding access they needed once, which is the finding our last two reviews both opened with.

## Proposal

Time-boxed grants requested at the moment of need and expiring automatically.

- A request flow that takes under a minute, with a required reason and a linked case
- Approval by the owning team, with a documented target of fifteen minutes during business hours
- Grants expire after four hours by default and cannot be extended silently
- A standing break-glass path with heavier logging and a mandatory review the next day

## Scope

Production data access for internal staff. Infrastructure access follows a different control and is out of scope.

## Risks

If approval is slow, people route around it, usually by holding a standing grant they justify once. The fifteen-minute target is the feature. If we cannot hit it, this proposal makes things worse rather than better, and we should know that before rolling it out broadly.

## Measurement

Standing grants outstanding, median approval time, break-glass uses per month, and whether the long tail of permanent access actually shrinks over two quarters.

## Rollout

The request flow and the approval target ship before any revocation. Asking people to request access through a path that is not yet fast is how routing around it starts, and once it starts it is a habit rather than a decision.

- Weeks one to three: request and approval live, standing grants untouched, approval time measured against the target
- Week four: the break-glass path and its next-day review
- Week five onward: revocation waves, only if the approval median has held

## Migration

Standing grants are revoked on a schedule rather than at once, ordered by how long since the holder last used them. Anyone who has not touched production data in six months loses it first and mostly will not notice, which is the point and the cheapest evidence that the long tail is real.

- Last-use data assembled per grant before anything is revoked, since the order depends on it
- Four waves over eight weeks, each announced a week ahead
- A grant revoked and then requested twice in a week flagged for review, because that pattern means the role needs standing access

## What Would Change Our Mind

If the approval median sits above fifteen minutes after three weeks of owning teams genuinely trying, the approval step is the wrong shape, and pre-approval by role with the same expiry keeps the time box while dropping the per-request judgment. If break-glass use climbs past a handful a month, four hours is too short for the real work, and lengthening it beats letting the exception become routine.
