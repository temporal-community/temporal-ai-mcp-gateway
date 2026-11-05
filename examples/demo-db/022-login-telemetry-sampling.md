---
Name: Login Telemetry Sampling
Owner: Hana Kobayashi
Status: Draft
Last Updated: 2025-12-27
---

## Background

We record every sign-in attempt with full context. The volume is now large enough that the storage cost is noticeable and the query performance on the security views is poor, which means the data we are paying to keep is the data nobody wants to wait for.

## Proposal

Sample successful routine sign-ins, keep everything else in full.

- Full retention for failures, challenges, unusual contexts, and anything involving a credential change
- Ten percent sampling for successful sign-ins from known devices in known contexts
- Aggregate counters retained at full fidelity so rates stay exact even where events are sampled
- Sampling decisions recorded, so a gap is distinguishable from an absence

## Non-goals

No change to the customer-visible activity view, which continues to show every sign-in to the account it belongs to.

## Risks

Sampling the successful path means losing detail exactly where a sophisticated attack would prefer to hide, since a successful sign-in from a known device is the goal state for an attacker. The classifier that decides what counts as routine is therefore a security control and needs to be reviewed as one, not treated as a cost optimization.

## Measurement

Storage volume, query latency on the security views, and whether any investigation in the following two quarters is impeded by a sampled gap.

## Rollout

Run the classifier in shadow for four weeks before a single event is dropped. It labels each sign-in routine or not, the label is stored, and everything is still retained in full. That gives the security team a labeled corpus to argue with, and it tells us what share of volume the routine class actually covers; if it is not the large majority, the storage saving does not justify adding a security control. Sampling then starts at fifty percent of the routine class rather than ten, and tightens only after two real investigations have run against sampled data without hitting a gap.

## Review Notes

- Classifier inputs and thresholds go through the same review as a detection rule, with a named approver on every change
- Known device needs a definition that cannot silently widen, since device identity is re-registered today on a browser profile reset
- Aggregate counters have to be dimensioned the way the security views group, or exact rates will not answer the questions people actually ask
- The sampling decision is written for retained events too, so the effective rate is verifiable after the fact rather than assumed

## Rollback

Turning sampling off is a configuration change and restores full retention immediately, but it does not undo anything: the events already discarded are gone, and an investigation reaching back into that window still meets the gap. Rollback therefore protects the future, not the period under review, which is the argument for starting at fifty percent and for holding the shadow weeks even when the storage line is uncomfortable.
