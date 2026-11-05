---
Name: On-Call Alert Noise Reduction
Owner: Nikhil Shah
Status: In Review
Last Updated: 2026-07-11
---

## Context

The on-call receives about ninety alerts a week, of which perhaps six require action. The rest are duplicates of the same underlying event, thresholds that were never tuned, or alerts for conditions that resolve themselves. People have started acknowledging without reading, which is the failure state this proposal exists to reverse.

## Proposal

Correlate, suppress, and delete, in that order.

- An AI correlation layer that groups alerts arriving from one underlying cause into a single incident, with the contributing alerts listed beneath
- Dependency-aware suppression, so a database alert suppresses the twelve service alerts that follow from it
- Every alert required to have an owner and a documented action, with unowned alerts deleted rather than inherited
- A monthly review of alerts that fired and were not acted upon

## Non-goals

No change to paging policy or rotation structure, which are separate conversations.

## Risks

Correlation that groups two genuinely separate incidents into one hides the second, and the second is the one nobody is looking at. Grouping must be visibly reversible from the incident view, and the correlation should favor leaving things separate when it is uncertain. We should also expect the model to learn from our alert history, which contains our bad thresholds as if they were signal.

## Measurement

Alerts per on-call week, share acted upon, time to acknowledge, and incidents where a correlated alert hid a separate cause, which should be zero and will not be.

## Sequencing

Deleting first is tempting, but the ownership sweep is what makes the other two steps safe: grouping alerts nobody owns produces an incident nobody owns. The order is ownership first, then dependency-aware suppression, which is deterministic and reviewable, then correlation over whatever still arrives. Running the correlation layer against the current ninety a week would mostly demonstrate that duplicates are duplicates, which we already know.

## Data We Have

Eighteen months of alert history with acknowledgment times, plus incident records that name a cause for the larger events.

- About nine thousand alerts, of which roughly one in fifteen was acted upon
- Acknowledgment timestamps, with no record of whether anyone read the alert
- Service dependency edges from the deployment graph, current for the request path and stale for batch jobs

The missing field is the one that matters most. We can tell that an alert was acknowledged and not that it was useful, so the monthly review has to supply that judgment by hand for the first few cycles.

## Failure Modes

Suppression keyed on a stale dependency edge hides a service alert whose database is healthy. A group that absorbs a slow-burning alert into a loud incident closes both when the loud one is resolved. The quietest failure is an alert tuned away for a condition that still happens, which the monthly review catches only if it reviews what did not fire alongside what did.
