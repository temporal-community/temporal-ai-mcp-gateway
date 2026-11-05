---
Name: Biometric Unlock for the App
Owner: Dmitri Volkov
Status: Approved
Last Updated: 2026-01-29
---

## Context

The application stays signed in indefinitely. Customers in regulated industries have asked for a local lock, and several have told us this is why the application is not permitted on their staff devices.

## Proposal

An optional local lock using the platform biometric mechanism, with a passcode fallback.

- Opt-in per device, or required by organization policy where the customer sets one
- Lock on background after a configurable interval, defaulting to five minutes
- The platform mechanism only, with no biometric data touching our systems
- Fallback to the device passcode, never to the account password

## Scope

Application unlock. This is not a second authentication factor and should not be described as one, since it protects against device access rather than credential theft.

## Risks

Describing this as security when it is convenience would be a mistake that someone will eventually make in a sales conversation. The documentation needs to state what it does and does not protect against, plainly, before the account team starts answering questions about it.

## Measurement

Adoption where optional, organizations enabling the policy, and unlock failures that end in a full sign-in, which is the frustrating path.

## Interfaces Affected

Organization policy is the part that reaches beyond the client. The policy document already carries session and device settings, so the lock requirement and its interval go there rather than into a new structure, and both appear in the admin console's policy diff.

- Policy gains two fields: whether the lock is required, and the interval
- The client reports lock capability at registration, so an admin can see which devices will fall back to a passcode
- Sign-out and token refresh are untouched; the lock sits above the session rather than inside it

## Failure Modes

The bad path is a locked application that cannot be unlocked: enrollment changed, the platform invalidated the key, and the device passcode no longer opens it. The application then has to sign the person out rather than strand them, and signing out discards unsent local changes. Unsent changes have to survive a forced sign-out, or this creates the data loss it was meant to prevent.

## Timeline

Policy enforcement lands a release after the opt-in setting, deliberately. Letting individuals turn the lock on first gives us real unlock-failure numbers before any organization can make it mandatory for its staff. A mandatory lock with an unknown failure rate is not something to put in front of a regulated customer.
