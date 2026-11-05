---
Name: Browser Extension Sign-In
Owner: Amara Osei
Status: Draft
Last Updated: 2025-11-18
---

## Problem

The browser extension authenticates by reading the session cookie of the main application. This breaks whenever a customer uses the extension in a profile where they are not signed in, which is common, and it ties the extension's lifetime to a cookie policy that is getting stricter every release of every browser.

## Proposal

Give the extension its own credential through a proper authorization flow.

- Standard authorization flow with proof of possession, opened in a tab rather than a popup
- Extension-scoped token with a narrow permission set, independent of the web session
- Refresh handled in the background worker with retry on wake
- Clear in-extension state when the credential is missing or expired, instead of silent failure

## Scope

The extension itself. The desktop application has a similar problem and is a separate piece of work with a different platform constraint.

## Risks

Extension credentials live in extension storage, which is readable by anyone with local access to the profile, so the scope has to be genuinely narrow rather than nominally narrow. We should not ship this with a token that can do everything the web session can.

## Measurement

Extension sign-in success rate, support contacts about the extension not working, and the share of extension sessions that survive a browser restart.

## Migration

Existing installations authenticate by cookie and cannot be upgraded quietly, because the new credential needs an action in a tab. The extension runs both paths for a period: cookie authentication continues where it works, and the first time it fails the extension opens the authorization flow instead of showing an error. Removing the cookie path is a later release, gated on the share of installations holding their own credential rather than on a date.

- Both paths live, cookie first, prompt on failure
- Cookie path removed once most installations hold their own token
- Installations that never complete the flow land in an explicit state, not a broken one

## Interfaces Affected

A genuinely narrow scope means naming the operations the extension performs, which has never been written down: today it inherits everything the web session can do. That list is the real design work, and it needs the authorization server to support a scope set the web session does not use. Revocation is the other new surface, since someone who removes the extension should be able to revoke its credential from account settings, which lists no connected clients at all today.

## Support Impact

The common contact now is an extension that silently does nothing, which support cannot diagnose without asking whether the person is signed in under a different profile. An explicit expired or missing state turns that into one readable answer. The new contact type is someone who declines the prompt and reports the extension as broken, which is rarer and easier to resolve.
