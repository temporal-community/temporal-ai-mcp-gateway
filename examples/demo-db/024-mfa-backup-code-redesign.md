---
Name: MFA Backup Code Redesign
Owner: Victor Alves
Status: In Review
Last Updated: 2026-03-11
---

## Problem

Backup codes are shown once at setup in a block of ten and never again. Support data suggests most people neither save them nor remember being shown them, so the codes exist mainly as a thing we can point to rather than as a working recovery path.

## Proposal

Treat backup codes as a deliberate step rather than a screen to click past.

- Codes presented one screen at a time with a required download or print action
- A confirmation step that asks for one of the codes before setup completes
- Regeneration available at any time, with the old set invalidated immediately
- A dashboard indicator when fewer than three codes remain unused

## Scope

The code mechanism itself. Whether codes are the right recovery factor at all is a question for the passkey work, which may make them unnecessary.

## Risks

Adding friction to security setup reduces completion of security setup, which is the oldest tradeoff in this area. If the confirmation step costs more enrollments than the codes save recoveries, it is a bad trade, and the test should be sized to detect that rather than assume it away.

## Measurement

Second-factor setup completion, recoveries completed with a backup code, and support cases where the customer had codes but could not find them.

## Rollout

The confirmation step is the only change that can cost enrollments, so it ships as a test with setup completion as the stopping metric and a sample large enough to see a single-digit drop. The rest goes to everyone: one screen at a time, the required download, regeneration, and the low-code indicator add nothing that can be failed. Testing the confirmation alone also keeps the result readable, since four changes at once would leave us guessing which one moved completion.

## Support Impact

The cases we get today are people with no second factor and no codes, which is the expensive path.

- Fewer identity-verification recoveries if codes are genuinely saved, which is the whole argument
- More contacts during setup in the first weeks, from people mistyping a code at confirmation
- Regeneration needs a plain warning that the old set stops working at once, or the case becomes a customer holding a printed sheet that no longer works

## What Would Change Our Mind

If the test shows the confirmation step costs more enrollments than the codes save recoveries, that step comes out and the rest stays. The other case is the passkey work. If passkeys reach enough of the base that recovery runs through a second device, this becomes maintenance on a path that is leaving, and the low-code indicator is the only piece worth carrying forward.
