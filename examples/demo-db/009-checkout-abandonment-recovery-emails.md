---
Name: Checkout Abandonment Recovery Emails
Owner: Omar Haddad
Status: Shipped
Last Updated: 2025-08-27
---

## Context

About a third of checkouts that reach the payment step are never completed. We send nothing afterwards. The growth team has asked for recovery email for two quarters and the blocker has been that checkout does not emit a durable event anyone can key off.

## Approach

Emit an abandonment event from checkout and drive a short, bounded email sequence from it.

- One email at one hour, a second at twenty-four hours, then nothing
- A deep link that restores the cart and the selected plan, valid for seven days
- Suppression for anyone who completed, cancelled, or contacted support in the window
- Hard unsubscribe honored before any send, not after

## Scope

Self-serve checkout only. Enterprise quotes have a human in the loop and do not need a reminder email.

## Risks

Recovery email is close to the line where helpful becomes unwelcome, and the reputational cost of getting it wrong is paid by every other email we send. The two-message cap is deliberate and should not be relaxed because the first test looks good.

## Measurement

Completed checkouts attributable to the sequence against a holdout, unsubscribe rate across all marketing email as a guardrail, and complaint rate per thousand sends.

## Rollout

Behind a holdout from the first send, since attributing recovered checkouts without one is guesswork. Start with the one-hour email alone for two weeks, and add the twenty-four-hour message only if the complaint rate per thousand sends stays flat against the rest of marketing email. The deep link ships with the first email or not at all, because a recovery message that drops someone at an empty cart is worse than no message.

## Failure Modes

- The event fires for someone who completed on another device, so a buyer is asked to finish a purchase they already made
- The seven-day link outlives a price change and restores a cart we no longer honor
- Suppression misses a support contact that arrived from a different address than the one used at checkout
- A retry at the payment step reads as a second abandonment and restarts the sequence

The last is the one to engineer against: two sequences for one checkout breaks the two-message cap.

## Review Notes

Growth asked for a third message at seventy-two hours and it was declined, on the ground that the cap is what keeps the reputational cost bounded rather than a parameter to tune on the first good result. Legal confirmed the deep link may carry nothing identifying the cart beyond an opaque token, and that hard unsubscribe is checked at send time, not at enqueue.
