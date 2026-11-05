---
Name: Flaky Test Quarantine
Owner: Lena Fischer
Status: In Review
Last Updated: 2026-07-14
---

## Context

About four percent of test runs fail for reasons unrelated to the change. Engineers retry by reflex, which means a genuine failure is also retried, and we have shipped at least two defects that a red build had correctly identified.

## Proposal

Detect flakiness automatically, quarantine it, and make quarantine uncomfortable.

- Flakiness detected by re-running failures on the same commit, recorded per test
- Tests exceeding a threshold quarantined: still run, no longer blocking
- An AI triage pass over quarantined tests that clusters them by probable cause and points at the likely culprit, so the backlog is actionable rather than a list
- Quarantine with an expiry, after which the test is deleted rather than left to rot

## Non-goals

No blanket retry policy. Retries hide flakiness, which is how we got here.

## Risks

Quarantine reduces pain, which reduces the pressure to fix, which is how a quarantine list becomes permanent. The expiry is the mechanism that prevents this and will be unpopular the first time it deletes a test somebody cared about. The clustering is an aid to prioritization and should not be treated as a diagnosis.

## Measurement

Flaky failure rate, quarantine list size and age, tests deleted at expiry, and retries per build, which should fall.

## Staffing

Quarantine without an owner is a list nobody reads. Each quarantined test is assigned to the team that owns the file it lives in, taken from the ownership file rather than from the commit history, since the last person to touch a test is often not the team that depends on it. Tests in shared directories with no owner go to the build team, which is the smallest group here and the reason the expiry matters more for that bucket than any other.

## Rollout

- Detection only for four weeks, recording per-test failure rates with nothing quarantined
- Threshold set from the observed distribution, not chosen in advance
- Quarantine enabled for one repository first, with expiry set long and shortened later
- The clustering step added last, once there is a backlog large enough for clusters to mean anything

Enabling quarantine and expiry together would delete tests before anyone has seen the list, so the expiry clock starts only after the first full review of what quarantine caught.

## Failure Modes

A test that fails because of a genuine defect intermittently looks exactly like a flaky one to the re-run detector, and quarantining it removes the signal that would have caught the defect. The detector's threshold is what separates the two, and setting it too low converts the two shipped defects in Context into a recurring category rather than a pair of incidents.

The clustering output is advisory, so a cluster that points at the wrong culprit costs a wasted investigation and nothing more.
