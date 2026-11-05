---
Name: First Response Time by Channel
Owner: Felix Braun
Status: Approved
Last Updated: 2026-04-20
---

## Problem

We report a single first-response figure across all channels. Chat responds in minutes and email in many hours, so the blended number describes neither and has been stable for a year while the email experience has measurably worsened.

## Proposal

Report and target per channel, with the target set from what customers expect of that channel.

- Separate targets for chat, email, and the in-product help path
- Business-hours and out-of-hours reported separately rather than blended
- Target attainment reported as a percentile rather than an average, since the tail is the experience people describe
- A weekly view by channel and by queue, visible to the whole team

## Non-goals

No change to staffing in this phase. The measurement should come first so staffing decisions have something to aim at.

## Risks

Publishing per-channel attainment will show one channel failing consistently, and the pressure will be to move people toward the measured failure rather than to the highest-value work. Targets should be set with that in mind and reviewed alongside resolution quality rather than alone.

## Measurement

Attainment per channel at the median and ninetieth percentile, and customer satisfaction by channel, watched together so that speed is not bought with quality.

## Data We Have

Inbound and first-outbound timestamps go back four years, so per-channel history can be restated without new collection. Restating it is also how the targets get set: chat's ninetieth percentile has sat under four minutes for two years while email's moved from eleven hours to nineteen, and the blended figure never shifted more than a few minutes.

- Business-hours boundaries per queue, which exist in the rota and have never been joined to ticket timestamps
- The in-product help path, with only nine months of history since it launched
- Reopen rates by channel, the nearest thing we have to a quality counterweight today

## Rollout

Restated history is published before any target is set, so the first conversation is about what has been true rather than what should be.

- Week one: the weekly view by channel and queue, with no targets drawn on it
- Week three: targets agreed per channel, with out-of-hours stated separately rather than exempted
- Week six: attainment against target, reported beside satisfaction in the same view

## Review Notes

Support leadership accepted the split and pushed back on the ninetieth percentile, arguing the tail is dominated by tickets waiting on a customer or on engineering. That holds for resolution time and not for first response, which is the metric here, so the percentile stays. The in-product path raised a separate point: nine months is too short to defend a target, so it reports without one for the first quarter.
