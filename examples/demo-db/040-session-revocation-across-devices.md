---
Name: Session Revocation Across Devices
Owner: Marcus Reyes
Status: In Review
Last Updated: 2026-01-30
---

## Problem

Signing out everywhere does not sign out everywhere. The web session is revoked immediately, mobile sessions expire when their access token does, and the desktop application keeps working until it next needs a refresh, which can be hours. For someone who has just lost a laptop, this is the wrong behavior.

## Proposal

Central revocation with a short, uniform propagation window.

- A revocation list checked on every token refresh and on a push channel for active clients
- Access token lifetime reduced to five minutes for all clients
- A visible device list with per-device revocation, not just a global switch
- Revocation events logged and surfaced in the security activity view

## Scope

First-party clients. Third-party integrations use separate credentials with their own revocation path, which already works correctly.

## Risks

Shortening token lifetime increases refresh traffic by roughly an order of magnitude on mobile, which is a cost and a reliability question for the token service. Load testing is a gate. There is also an offline behavior question: a client that cannot reach us cannot learn it has been revoked, and we should state that limit plainly rather than imply otherwise.

## Measurement

Time from revocation to last successful request per client type, refresh request volume, and support contacts about devices that would not sign out.

## Dependencies

The push channel is the piece we do not own. Mobile delivery goes through the same notification path as product messages, which is best-effort and gives us no receipt we can read. Desktop has no push channel today, so its refresh interval is its real propagation window until one exists. The token service team has to accept the new refresh volume before the five-minute lifetime ships, and the device list needs a stable device identifier, which mobile has and web approximates with a cookie a user can clear.

## Failure Modes

- Push delivered to a backgrounded client that ignores it, so revocation waits for the next refresh
- Revocation list unreachable at refresh time, with clients failing closed and signing out healthy sessions
- A reinstalled application appearing as a new device, so the list grows and the real device is hard to find
- Client clock skew extending an access token past its five minutes

Failing closed is the right default, and it turns a list outage into a mass sign-out, so the revocation list needs its own availability target rather than inheriting the token service's.

## Rollback

Token lifetime is a configuration value and can be returned to its current setting in one deploy, which also reverts the refresh traffic. The revocation list and the device view can stay up while that happens, since both are additive. What does not roll back cleanly is the expectation: a security activity view that shows revocation events and then stops showing them reads as a regression, so that view ships last.
