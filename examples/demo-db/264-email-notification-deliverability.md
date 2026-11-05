---
Name: Email Notification Deliverability
Owner: Clara Benton
Status: Approved
Last Updated: 2026-06-30
---

## Context

Our transactional and notification email share a sending domain. Notification volume is high and engagement is low, which has gradually degraded our reputation to the point where password resets and receipts are landing in spam folders for some recipients.

## Proposal

Separate the streams and manage each one's reputation deliberately.

- Transactional mail on a dedicated subdomain with its own reputation
- Notification mail on a separate subdomain, with engagement-based suppression
- Authentication records correct and monitored for all sending domains
- Reputation monitored per stream with alerting on degradation

## Scope

All outbound mail from the product. Marketing mail is already on a separate domain and stays there.

## Risks

A new sending domain starts with no reputation and must be warmed gradually, during which deliverability is worse than the current state. The warming plan has to be real, with volume ramped over weeks, and the transition must not happen alongside a high-volume campaign.

## Measurement

Inbox placement per stream, spam complaint rate, bounce rate, and support contacts about password reset mail not arriving, which is the symptom that prompted this.

## Rollout

Transactional first and alone. It is the smaller volume, it is the stream that is actually hurting, and it can be warmed by moving recipients in cohorts rather than by sending anything extra. Notification mail follows, and it is the easier warm because the volume ramps quickly.

- Weeks 1-2: authentication records published and verified for both subdomains
- Weeks 3-6: transactional recipients moved in cohorts, placement watched per cohort
- Weeks 7-10: notification mail moved, engagement suppression on from the first day
- The old domain is left idle rather than retired until both streams are stable

## Rollback

Pointing a stream back at the shared domain is a configuration change and takes minutes, which makes rollback cheap and misleading. The reputation damage that prompted this does not reverse in minutes, and a stream moved back and forth builds reputation on neither domain. The decision point is per cohort during the warm, and reverting a cohort means restarting its warm rather than resuming it.

## Open Questions

What engagement-based suppression means for notification mail is unsettled. Dropping a recipient who has not opened anything in ninety days protects the sending reputation and also stops sending someone a notification they asked for. The categories where that is unacceptable have not been listed.
