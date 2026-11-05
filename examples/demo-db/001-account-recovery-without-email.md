---
Name: Account Recovery Without Email
Owner: Ben Tsai
Status: Parked
Last Updated: 2025-09-25
---

## Problem

Every recovery path ends at the registered email address. When that address is itself inaccessible, which is the common case for people recovering from a compromise or leaving an employer, the only route is a support case resolved by judgment rather than by policy.

## Proposal

A documented recovery path that does not depend on inbox access.

- A recovery contact nominated in advance who can attest to a request
- Verification against payment method details already on file
- A mandatory waiting period with notification to every channel on the account
- A written policy for what support may and may not do, replacing current judgment

## Scope

Individual accounts. Organization accounts recover through their administrators and, failing that, through the contract owner.

## Risks

This is the most attacked path in any identity system, because it is designed to work when the normal credentials do not. Every convenience added here is also available to an attacker, and the waiting period is the only control that cannot be socially engineered. Parked pending a security design review, which should happen before any further design work rather than after.

## Measurement

If it proceeds: recovery cases resolved by policy rather than judgment, median time to recovery, and recovery-initiated takeovers, which must stay at zero.

## Support Impact

Recovery today is a judgment call made by whoever picks up the case, and the person making it carries the risk personally. A written policy moves that risk off the individual, which is the change support staff will value most. It also removes their ability to say yes to a sympathetic case that does not fit the policy, and the first quarter will produce escalations that are really appeals against the rules. Those need a route other than asking the same reviewer twice. Handling time rises too: a case that ends today in a thirty-minute decision instead stays open for the whole waiting period, with contact from the customer at intervals.

## Prior Art

The recovery contact pattern and attestation by an enrolled device both exist in published consumer identity policies, and the consistent lesson is that no single factor is treated as sufficient. Closer to home, the billing dispute flow already verifies the last four digits and the billing postcode, so payment verification is not new ground here. The fraud team's assessment of how much that proves should be taken as input to the security review rather than re-derived by this project.

## Open Questions

- Whether a recovery contact can be nominated during a recovery rather than in advance, which is convenient and almost certainly unsafe
- What happens to a dormant account whose payment method expired years ago, which describes a large share of the accounts that need this
- Whether notifying every channel on the account is itself usable by an attacker as a probe
