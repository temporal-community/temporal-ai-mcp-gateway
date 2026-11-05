---
Name: Push Notification Batching
Owner: Maya Brennan
Status: Approved
Last Updated: 2026-02-16
---

## Context

A busy workspace generates a notification per event. During an active discussion this means six or seven pushes in a minute, which is why our notification opt-out rate on mobile is roughly twice the industry figure people quote at conferences.

## Proposal

Batch notifications within a short window and summarize rather than enumerate.

- A thirty-second collection window per conversation, extended while activity continues
- A single summary push describing what happened, not a list of each thing
- Direct mentions bypass batching, because those are the ones people want immediately
- Per-category controls that are genuinely granular, replacing the current all-or-nothing switch

## Non-goals

No change to email notification, which has its own cadence problem and its own audience.

## Risks

Batching introduces latency into notifications people have told us they want fast, and the thirty-second window will feel wrong to somebody. The mention bypass is what makes this acceptable; without it, batching would be a straightforward downgrade for the most engaged users.

## Measurement

Pushes per active user per day, notification opt-out rate, and open rate per push, which should rise as volume falls. If opens fall with volume, the batching is hiding things people wanted.

## Rollout

The granular category controls ship first and alone. They are what people have asked for directly, they cut volume for anyone who uses them without adding a second of latency, and they establish how much of the opt-out rate was volume rather than relevance. Batching follows behind a flag, limited to workspaces above a message-rate threshold where the problem actually exists. A quiet workspace gains nothing from batching and pays the full thirty seconds anyway.

## Interfaces Affected

- The notification service, moving from per-event sends to a windowed queue holding state per conversation
- Badge counts and the in-product list, which have to stay per-event even when the push is a summary, or the two will visibly disagree
- Mention detection, which now gates latency as well as content, so it must be fast and must not be wrong
- The settings screen, where replacing one switch with categories is a migration for everyone who has already switched it off

## What Would Change Our Mind

If opt-outs drop once the category controls ship and before any batching exists, the problem was relevance rather than volume, and the thirty-second window buys complaints for very little. The other direction is worth watching just as closely: if opens per push fall as volume falls, the summaries are hiding something people wanted, and the answer is the content of the summary rather than the length of the window.
