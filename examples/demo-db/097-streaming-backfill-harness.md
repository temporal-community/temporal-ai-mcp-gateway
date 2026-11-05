---
Name: Streaming Backfill Harness
Owner: Dana Whitfield
Status: Draft
Last Updated: 2025-11-29
---

## Background

When a streaming job has a bug, fixing the code does not fix the data. Backfilling means writing a one-off batch job that reimplements the streaming logic, which is how we end up with two implementations that disagree about edge cases.

## Proposal

A harness that replays historical events through the current streaming logic into a shadow output.

- Replay from the retained event log at controlled speed, with the same code path as live
- Output to a shadow table, diffed against live before any swap
- Swap as an atomic rename once the diff is understood and accepted
- Progress and lag visible, because a full replay takes days

## Scope

Jobs on the stream processing framework. The two remaining custom consumers are out of scope and should be migrated rather than accommodated.

## Risks

Replay at speed is a load test of everything downstream, including the operational stores that some jobs write to. Rate limiting is part of the harness rather than an operational practice, because the first person to forget it will cause an incident during a routine backfill.

## Measurement

Time to correct a day of bad data, the number of one-off backfill jobs written per quarter, and whether any of the diffs reveal a discrepancy nobody expected, which would justify the harness on its own.

## Dependencies

Replay reaches back only as far as the event log, and retention differs by topic: thirty days on most, seven on the two highest-volume ones, which also run the most complex jobs. A backfill older than retention is out of reach and should be stated as such rather than discovered mid-incident.

- Per-topic retention, published where someone planning a backfill will see it
- Deterministic job logic, since a job reading current state rather than event state cannot reproduce history
- Shadow table provisioning, which doubles storage for the length of a replay
- The rate limiter, in the harness path rather than configured per run

## Failure Modes

The dangerous case is a job that is non-deterministic in a way nobody noticed. One that enriches events with an account's current tier produces a shadow output correct against today and wrong against the day replayed, and the diff will not flag it, because live is wrong in the same places for different reasons. Listing each job's external reads before its first replay is the only practical guard. The second is the swap: an atomic rename is atomic for the table and not for a consumer holding a long read across it, which gets half of each.

## Rollback

Before the swap there is nothing to roll back, which is most of the value of a shadow output. After it, the previous table still exists under its renamed name and can be swapped back, and that is the whole argument for rename over writing in place. The recovery lasts only while the old table is kept, so the harness retains it for a stated period rather than until someone tidies up.
