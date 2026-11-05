---
Name: Trial Length Experiment Framework
Owner: Priya Raman
Status: Draft
Last Updated: 2025-11-16
---

## Background

Our trial has been fourteen days since the beginning. The number was chosen because it is a common number. Nobody has tested it, and the activation data suggests a meaningful share of workspaces are still evaluating when it ends.

## Proposal

A framework for testing trial length safely, then a sequence of tests.

- Trial length as a configurable attribute on the account rather than a constant
- Assignment at signup, recorded immutably, so analysis is not confounded by later changes
- Guardrails on revenue per signup, not just conversion rate
- A fixed analysis window long enough to capture post-trial conversion, which lags

## Scope

Self-serve trials. Enterprise evaluations are negotiated and are not affected.

## Risks

Trial length tests are slow, because the outcome is only visible after the longest arm completes plus a conversion lag. A premature read will favor the shorter arm, which converts sooner, and that reading will be wrong in a way that is expensive to undo.

## Measurement

Conversion rate and revenue per signup by arm, time to activation within the trial, and the share of conversions occurring after the current fourteen-day point.

## Sequencing

The framework ships before any arm runs. Trial length has to become an account attribute, the existing population has to be backfilled with fourteen, and the immutable assignment record has to survive a plan change. An arm run before that record is trustworthy produces a result nobody will believe.

- First test: fourteen against thirty, the widest gap we would actually ship
- Second test: the winner against the midpoint, and only if the first clears the guardrail
- No arm shorter than seven days until we see where activation lands inside the current fourteen

## Dependencies

Billing has to accept a per-account trial end date rather than deriving it from the signup date. Lifecycle messaging keys off that same date and sends on days three, ten, and thirteen, so those sends move with the arm or the short arms get a different message cadence instead of a different trial length. The warehouse signup snapshot also has to carry the assigned length, since reading it live from the account returns the current value rather than the assigned one.

## Open Questions

- Whether the analysis window runs from signup or from trial end, given a thirty-day arm pushes the read out by sixteen days
- What happens to a workspace mid-trial when its arm is retired
- Whether revenue per signup is read at ninety days or at first renewal
