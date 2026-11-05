---
Name: Shared Mailbox Access Model
Owner: Caleb Mortensen
Status: Parked
Last Updated: 2025-10-21
---

## Context

Several customers run their account from a shared mailbox, with four or five people using one set of credentials. Our model has no way to express this, so it shows up as a single user with impossible behavior and as a security finding we cannot act on.

## Proposal

Recognize shared access explicitly rather than pretending it does not happen.

- A shared account type with individual sign-in but a common inbox for notifications
- Per-person attribution on every action, so the activity log is meaningful
- Notification routing configurable per event type rather than all to one address
- A migration path from the current single-credential pattern that does not interrupt access

## Scope

Account structure and notification routing. Billing ownership and contract signatories are separate questions.

## Risks

This legitimizes a pattern we would rather discourage, and the effort may be better spent making individual accounts with proper roles easy enough that nobody wants a shared mailbox. Parked while we interview the affected customers, because the proposal assumes a motivation we have not actually verified.

## Measurement

If it proceeds: shared-credential accounts detected by behavior, attribution coverage in activity logs, and whether affected customers move voluntarily.

## Alternatives Considered

Making individual accounts cheap enough that nobody wants a shared mailbox is the alternative the risks name, and it is a different project: seat pricing, invitation flow, and role definitions, none of them owned here. The second option is detection without accommodation, flagging accounts whose behavior indicates shared credentials and asking them to split. That is cheap, worsens the relationship with customers doing this deliberately, and leaves the activity log as useless as it is now.

## Support Impact

A support contact from one of these accounts cannot be matched to a person today, so password resets and permission questions are answered to whoever reads the mailbox. That is the concrete harm, and it is worth recording while the work stays parked: not only a security finding, but a handful of interactions a month that cannot be verified. Any version that ships has to let support see which person acted.

## What Would Change Our Mind

The customer interviews decide it. If the motivation is cost, the answer is pricing and this stays parked. If the work genuinely belongs to a desk rather than a person, a duty inbox staffed in shifts for instance, individual accounts do not solve it however cheap they get, and shared access with attribution is the right shape. If nobody chose this and the credential was simply never split, the answer is migration tooling and nothing more.
