---
Name: Step-Up Verification for Sensitive Actions
Owner: Dmitri Volkov
Status: In Review
Last Updated: 2026-07-21
---

## Context

Changing a payout destination, removing a second factor, and exporting all workspace data are all protected by nothing more than holding a session. An attacker with a stolen session can do all three in under a minute, and our incident history includes exactly that sequence.

## Proposal

Require fresh verification for a defined set of sensitive actions.

- A list of sensitive actions defined centrally rather than decided per feature
- Re-verification valid for ten minutes, so a sequence of related changes does not prompt repeatedly
- Passkey or second factor accepted, password alone never sufficient
- An AI assistant in the security console that explains to administrators why a particular action required verification, drawing on the policy rather than guessing

## Scope

The first list covers payout changes, credential changes, bulk export, and permission escalation. The list is expected to grow and the mechanism should make growing it a configuration change.

## Risks

Protecting too much trains people to approve reflexively, which is how step-up verification stops working. The list should stay short and each addition should have to argue for itself. The assistant must read from the policy definition rather than describing behavior it infers, or it will confidently explain rules that do not exist.

## Measurement

Sensitive actions preceded by verification, takeover incidents involving one of the listed actions, and prompt fatigue measured as approval latency over time.

## Interfaces Affected

A central list means each protected action asks one component instead of deciding for itself.

- Payout settings, credential settings, export, and the permission paths each call the check and handle a not-verified result rather than returning a generic error
- The verification prompt, which has to work with a passkey and with a second factor and must not offer the password fallback that sign-in does
- The security console explainer, which reads the policy definition and so requires that definition to be data rather than code
- Programmatic paths, where a token-authenticated call cannot be re-verified interactively and needs an explicit answer

## Failure Modes

An account whose only factor is the one being removed, where verification for that removal is impossible and the recovery path must not become a weaker route to the same action. A ten-minute window opened for one change that then carries a second, unrelated sensitive action nobody intended to authorize. And the explainer describing a rule that changed after its last read, which is the failure the risks section names and is prevented by reading the policy at request time rather than caching it.

## Open Questions

What a programmatic call does when it reaches a protected action. Refusing is consistent and breaks automation that legitimately changes permissions; allowing it leaves a route around the control for anyone holding a token. We have also not decided whether the ten-minute window is per action type or global, where global is friendlier and turns one verification into permission across the whole list.
