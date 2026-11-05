---
Name: Fraud Review Queue Triage
Owner: Lena Fischer
Status: In Review
Last Updated: 2026-05-08
---

## Context

Transactions flagged by the rules engine go to a single review queue, ordered by arrival. Reviewers work through it in order, which means a straightforward case blocks a complex one and a high-value case waits behind a trivial one. Queue time at peak reaches six hours.

## Proposal

Prioritize and pre-assess the queue so reviewer attention goes where it matters.

- Ordering by value at risk and by time sensitivity rather than by arrival
- An AI risk scoring pass that summarizes the case and highlights the specific signals that triggered the flag
- Clear-cut cases on either extreme routed to automatic decisions, with sampling to verify
- Reviewer decisions recorded with their reasoning, feeding both rule tuning and model evaluation

## Scope

Transaction review. Account-level fraud investigation is a different workflow with longer timelines.

## Risks

Automatic decisions at the extremes are where this saves time and where an error is unreviewed by anyone. The sampling rate on auto-decided cases has to be high enough to detect drift quickly, and the score must never be the only input to a decision that blocks a legitimate customer's money. Reviewers reading a summary before the evidence will also tend to confirm it, so the interface should present the signals and not a conclusion.

## Measurement

Queue time by case value, decision accuracy on sampled automatic decisions, reversal rate on appeal, and fraud loss against the baseline.

## Rollout

Reordering the queue is independent of everything else and ships first. It needs no scoring pass and no automatic decisions, and it addresses the six hours directly: a high-value case waiting behind trivial ones is a prioritization problem, not a capacity problem. Scoring follows, presented as signals with no recommendation attached. Automatic decisions come last, and at one extreme to begin with.

- Reorder by value at risk and time sensitivity, nothing else changed
- Scoring and signal highlighting, reviewers still deciding every case
- Automatic clearing at the low-risk extreme, heavily sampled
- Automatic blocking at the high-risk extreme only after the low end has run clean for a quarter

Starting at the low-risk end is deliberate. A wrongly cleared transaction costs money; a wrongly blocked one costs a customer, and that is the harder one to undo.

## Staffing

Reviewer time does not drop in the first phase. It moves to the cases that deserve it, which is the point. The new standing cost is the sampling review, and it needs a senior reviewer rather than any reviewer, because the question is whether a decision was right rather than what the decision should be. Rule tuning from recorded reasoning also needs an owner on the rules engine side, work that has historically happened whenever someone had time.

## Open Questions

The sampling rate is unset, and it is the number that decides whether automatic decisions are safe at all. Appeals are also unsettled: a customer appealing an automatic block should reach a person, and whether that person sees the score before the evidence is the same ordering problem the Risks section raises for the queue.
