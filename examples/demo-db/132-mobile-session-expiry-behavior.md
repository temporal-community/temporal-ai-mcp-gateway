---
Name: Mobile Session Expiry Behavior
Owner: Omar Haddad
Status: Draft
Last Updated: 2026-01-11
---

## Context

When a mobile session expires, the application drops to the sign-in screen and discards whatever the person was doing. For someone who opened the application to check one thing, this is a full sign-in for a ten-second task, and it is the most common complaint in our application store reviews.

## Proposal

Refresh silently where we can and preserve context where we cannot.

- Token refresh in the background before expiry rather than on failure
- On genuine expiry, preserve the current screen and restore it after sign-in
- Unsent input held and restored, not discarded
- A clear explanation when expiry was caused by a revocation rather than by time

## Scope

Session handling in the mobile applications, coordinated with the revocation work so the two do not fight.

## Risks

Preserving context across a sign-in means holding state across an identity boundary, and if the person who signs in is not the person who was there before, restoring that state is a disclosure. The restore must be conditional on the same account signing in.

## Measurement

Sign-ins per active user per week, task abandonment at the sign-in screen, and store review mentions of being signed out.

## Dependencies

Background refresh needs the application awake before the token expires, which neither platform guarantees: a backgrounded application may get no execution time for hours. The practical rule is to refresh on foreground as well as on a timer, treating the timer as an optimization rather than the mechanism. The revocation work owns the other half, since a refresh that succeeds against a revoked session is worse than an expiry.

- Refresh on foreground, timer as the secondary path
- Revocation signal reaching the application before it attempts a refresh
- Preserved state scoped to an account identifier, never to the device

## Failure Modes

Holding unsent input across a sign-in leaves that input in device storage for the duration, which for a draft containing something sensitive is a longer exposure than the person expects. It has to clear on explicit sign-out and on sign-in by a different account, and both need testing rather than assuming, because the second is the case nobody exercises by hand. The other failure is a refresh loop: a token that refreshes successfully and is still rejected leaves an application that looks signed in and does nothing.

## Timeline

Background refresh first. It removes most expiries and carries no state-restoration question. Context preservation follows once account scoping is implemented and tested. The revocation explanation goes last, since it depends on a signal the other work has to publish first.
