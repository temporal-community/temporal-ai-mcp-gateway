---
Name: Chat Queue Prioritization
Owner: Grace Lindqvist
Status: Draft
Last Updated: 2025-08-16
---

## Context

Chat is first come, first served. During busy periods a customer with a two-minute question waits behind a complex case, and a customer locked out of their account waits behind a general enquiry. Wait time variance is high and unrelated to urgency.

## Proposal

Prioritize on urgency and expected handling time, with a cap on how long anyone waits.

- Urgency inferred from the opening message and the account state, such as a failed payment or a locked account
- Short questions identified and routed to a fast queue, which also improves throughput
- A maximum wait regardless of priority, after which the ticket rises to the top
- Wait time shown to the customer honestly, including when it is long

## Non-goals

No priority by plan tier in this phase. That is a commercial decision rather than an operational one and should be made deliberately if at all.

## Risks

Inferring urgency from an opening message rewards customers who learn the right words, and penalizes the understated. The maximum wait is what bounds the damage, and it should be short enough to matter.

## Measurement

Wait time at the median and ninetieth percentile, abandonment rate, and whether urgent cases measurably reach someone faster without the tail getting worse.

## Failure Modes

Account state is the reliable signal and the opening message is not. A locked account or a failed payment is a fact; a customer writing that something is urgent is a claim. Weighted equally, the inference becomes a keyword game within a month of the first person noticing. Account state should dominate, with the message able to raise priority one step and no further.

The honest wait display has its own failure. A long estimate shown accurately will raise abandonment, and abandonment is one of the measures. Someone who leaves because they were told forty minutes has not been served, and counting that as a win because the queue got shorter is the wrong reading.

## Sequencing

The maximum wait goes in first, on the existing first-come queue. It is the only part that strictly improves current behavior, it needs no inference, and it gives a clean baseline for the tail before prioritization starts moving it.

- Maximum wait live on the current queue, tail measured for two weeks
- Fast queue next, split on expected handling time alone
- Urgency inference last, account state first and message signals added separately

## Staffing

The fast queue needs people assigned to it rather than drawn from the same pool, or it is a label on the same wait. That is a scheduling change: two or three people on short questions during busy periods, which is also when the complex-case queue is longest and losing them hurts most.
