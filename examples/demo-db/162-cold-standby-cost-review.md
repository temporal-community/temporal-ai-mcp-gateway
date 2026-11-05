---
Name: Cold Standby Cost Review
Owner: Amara Osei
Status: Parked
Last Updated: 2025-10-01
---

## Background

The secondary region runs a warm standby of every service at thirty percent capacity. It costs about a sixth of total infrastructure spend and has been used in anger once, for twenty minutes, in three years.

## Proposal

Review the standby posture per service against its actual recovery requirement.

- Services classified by recovery objective: minutes, hours, or next business day
- Warm standby retained only for the minutes class
- Hours-class services moved to cold standby with tested provisioning automation
- The remainder relying on backup restore, verified by the restore program

## Scope

The secondary region posture. Data replication is unaffected and stays as it is.

## Risks

Cold standby is only cheaper if the provisioning automation works, and automation that is never exercised is not automation. Moving a service to cold standby without a tested provisioning path converts a cost saving into an availability risk that will not be visible until it matters.

Parked until the failover drill program has run twice, since the drills will tell us whether the automation is trustworthy. Deciding this before that evidence exists would be guessing.

## Measurement

If it proceeds: infrastructure spend on the secondary region, provisioning time per cold-standby service, and recovery objective attainment during drills.

## Data We Have

The one real failover, twenty minutes three years ago, is a single data point, and the services that carried it would stay in the minutes class under any version of this proposal. What we do not have is a measured provisioning time for any service starting from cold. The first two drills will produce that number for the six services in their scope, and every estimate here is an estimate until they do. Per-service spend in the secondary region we do have, and it is lopsided: four services account for most of the sixth, three of which look hours-class on inspection.

## Dependencies

- Two completed failover drills, which is the condition this is parked on
- A recovery objective agreed per service with the team that owns it rather than assigned centrally
- Provisioning automation living in each service's own repository, so it breaks the owning team's build when it rots
- Restore program verification, which today covers only some of the datastores behind the next-business-day class

## What Would Change Our Mind

If the drills show cold provisioning overrunning an hours-class objective because of image build time rather than configuration, the saving is still real but reaching it becomes a build-pipeline project with its own cost, and the comparison changes. The reverse also holds: if warm standby at thirty percent turns out not to absorb a regional failover without scaling first, the minutes class is paying for a guarantee it does not have, and the review becomes urgent rather than parked.
