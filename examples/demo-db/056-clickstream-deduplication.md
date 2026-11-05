---
Name: Clickstream Deduplication
Owner: Amara Osei
Status: Approved
Last Updated: 2026-04-28
---

## Problem

The mobile clients retry event delivery on poor connections without idempotency keys, so a subset of sessions produce duplicate events at a rate that varies with network conditions. Every count built on clickstream is therefore inflated by an unknown, moving amount, which is worse than being inflated by a known one.

## Proposal

Deduplicate at ingest on a client-generated event identity, and measure what we remove.

- Clients generate a stable identity per event, persisted across retries and restarts
- Ingest keeps a rolling window of seen identities sized to the longest plausible retry
- Duplicates counted and reported by client version and network type
- Historical data annotated rather than rewritten

## Scope

Mobile and web clickstream. Server-side events already carry a request identity and are not affected.

## Risks

The rolling window is a memory-for-correctness trade. Too short and late retries pass through; too long and ingest becomes expensive. The duplicate rate by client version will tell us where to set it, which means shipping the measurement before the enforcement.

## Measurement

Duplicate rate before and after, variance in daily active counts against a server-side control, and the gap between clickstream and server-side session counts, which should narrow.

## Sequencing

Measurement ships first and enforcement second, with at least four weeks between them so the duplicate rate is observed across a full release cycle of the mobile clients. The window size is chosen from that observation rather than guessed, and until it is chosen ingest marks duplicates without dropping them.

- Identity generation in the clients, behind the normal release train
- Ingest marks and counts duplicates, drops nothing
- Window sized from the observed retry distribution, ninety-ninth percentile
- Enforcement enabled per event type, starting with session start

## Migration

Old client versions will keep sending events without an identity for as long as they remain installed, and the long tail on mobile is measured in quarters. Events without an identity pass through unchanged, so the duplicate rate falls gradually rather than at a cutover, and any comparison across the transition has to be read against client version share.

Historical data is annotated, not rewritten, which means every count built before enforcement remains inflated. A dashboard that spans the boundary shows a step that is a measurement change rather than a behavior change, and the annotation is what stops it being read as one.

## Cost

The rolling window of seen identities is the whole ongoing cost of this change, and it scales with event volume times window length. Sizing it from the ninety-ninth percentile rather than the maximum retry delay keeps it affordable and lets a small number of very late retries through, which is the trade the Risks section describes.
