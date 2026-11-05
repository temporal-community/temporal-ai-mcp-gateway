---
Name: Runbook Coverage Gaps
Owner: Victor Alves
Status: Approved
Last Updated: 2026-06-09
---

## Context

About half our alerts link to a runbook. Of those, an unknown number are stale, because the only way to find out is to follow one during an incident, which is the worst time to discover it describes a system that no longer exists.

## Proposal

Measure coverage, generate first drafts for the gaps, and verify what exists.

- Coverage measured per alert, reported per team, with no runbook treated as a defect
- An AI drafting pass that produces a first runbook from the alert definition, recent incidents, and the service's own documentation, for a human to correct rather than to start from nothing
- Every runbook carrying a last-verified date, set by someone following it, not by someone editing it
- Runbooks unverified for two quarters flagged on the alert itself

## Non-goals

No mandate that every alert have a runbook. Some alerts should be deleted instead, and the coverage report should make that an acceptable answer.

## Risks

A generated runbook is a plausible document about a system the model has only read about, and during an incident plausible is dangerous. Drafts must be visibly marked unverified until a human has followed them, and we should measure how many drafts survive first contact.

## Measurement

Alerts with a verified runbook, runbooks verified per quarter, and time to first useful action during incidents where a runbook existed.

## Sequencing

Coverage measurement runs alone for a quarter. The report pushes some teams to delete alerts rather than write runbooks, which is the cheapest coverage improvement available and stops being available once a draft exists for everything.

- Quarter one: coverage per alert per team, plus the alert deletion pass the report provokes
- Quarter two: drafting for the remaining gaps, marked unverified, with verification counted separately from existence
- Quarter three: the two-quarter staleness flag turns on, by which point the verified set is large enough for the flag to mean something

## Staffing

Verification is the scarce resource, since it has to be done by someone who could run the incident, and that is the same small group already on call. Following a runbook end to end against a staging failure takes about an hour, which across roughly four hundred alerts is more hours than a quarter holds. Verifying in severity order rather than alphabetically is what makes the first pass useful, and it means low-severity alerts stay unverified for a long time.

## Failure Modes

The failure that matters is a draft verified by reading it. A responder who skims a generated runbook, sees nothing obviously wrong, and sets the date has produced something worse than an unverified draft, because the unverified mark was the warning. Verification should require recording what was run and what came back, and one with no commands recorded should not count. The slower failure is a runbook verified once while the system drifts under it, which is why the staleness flag sits on the alert rather than on the document nobody opens.
