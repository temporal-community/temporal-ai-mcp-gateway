---
Name: Feature Flag Hygiene
Owner: Victor Alves
Status: Approved
Last Updated: 2026-07-20
---

## Context

We have four hundred and twelve flags. About sixty are doing real work; the rest are fully rolled out, fully off, or forgotten. Each one is a branch in the code and a line in the evaluation path, and several have been on for so long that removing them is genuinely risky.

## Proposal

Make flags expire by default and make removal routine.

- Every new flag carrying a type at creation: release, experiment, or permanent
- Release and experiment flags expiring, with the owner notified before and at expiry
- Expired flags blocking deploys for their service until resolved, which is the only mechanism that has ever worked for this
- Permanent flags reviewed annually and justified

## Scope

The shared flag system. Flags embedded in configuration files are a separate cleanup.

## Risks

Blocking deploys on flag expiry puts a cleanup task in the path of urgent work, which will occasionally be exactly the wrong time. A grace extension that costs one click and is recorded gives the escape valve without making expiry meaningless.

## Measurement

Total flag count, median flag age by type, flags removed per month, and deploys blocked by expiry, which should be frequent at first and rare within two quarters.

## Migration

The existing three hundred and fifty-odd flags do not get typed centrally. Each is attributed to the service that evaluates it and appears in that service's queue with no expiry set until its owner classifies it, so classification is what starts the clock. The roughly forty with no identifiable owner, mostly created by people who have since left, fall to the service's on-call rotation. That is unfair to whoever is holding the pager, and it is still better than a central list nobody owns.

## Alternatives Considered

- A quarterly cleanup sprint, which we ran twice; the count fell by about sixty each time and was back within a quarter
- A stale-flag dashboard with no enforcement, which exists and was opened eleven times last quarter
- Removal at expiry without a human, rejected because removing a flag means deleting one side of a branch and nothing can decide which side
- A per-service cap on new flags, which taxes the next flag instead of the four hundred already here

## Timeline

Typing and expiry metadata land first and change nothing for anyone. Owner notifications follow two weeks later. Deploy blocking turns on four weeks after that, and the gap is the point: no team should meet this proposal for the first time in a blocked deploy. Permanent-flag review starts a quarter out, once the count has stopped moving and the remaining list is small enough to argue about one flag at a time.
