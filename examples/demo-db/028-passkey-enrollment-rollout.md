---
Name: Passkey Enrollment Rollout
Owner: Dana Whitfield
Status: Approved
Last Updated: 2026-03-19
---

## Context

Password-based sign-in accounts for the majority of our account takeover cases and nearly all of our support volume around access. Passkey support shipped behind a flag last quarter and has about four hundred voluntary enrollments with no reported problems.

## Proposal

Move passkeys from opt-in to the default path for new accounts and prompt existing ones.

- New accounts enroll a passkey during setup, with password as an explicit fallback
- Existing accounts prompted after a successful sign-in, dismissible and rate-limited to once a month
- Recovery through a second passkey or a verified recovery contact, never through password reset alone
- Clear device-loss guidance written before launch, not after

## Non-goals

No removal of password sign-in in this phase. Removing it is the point eventually, but not while recovery still has rough edges.

## Risks

Device loss is the whole risk. A customer with one passkey on one device who loses it must not be locked out of their business, and the recovery path is harder to design than the enrollment path. The second-passkey prompt is therefore part of enrollment rather than a later nudge.

## Success metrics

Share of sign-ins using a passkey, account takeover cases per month, and access-related support contacts, with lockout rate watched closely as the guardrail.

## Data We Have

Four hundred voluntary enrollments with no reported problems is encouraging and is also the least representative population available: people who opt into a security feature behind a flag tend to own current devices and understand exactly what they enrolled. The number worth pulling is how many of those four hundred added a second passkey, since that tells us whether the second-device prompt lands when nobody is obliged to answer it. Platform mix is the other gap. The flagged cohort skews to one operating system, and device-loss behaviour is where platforms differ most.

## Rollout

New accounts go first, because there is no habit to interrupt and setup is the one place where enrolling is not an interruption. Existing accounts follow in cohorts ordered by sign-in recency: a prompt is cheapest to show someone who signs in weekly, and most likely to be mishandled by someone returning after six months who no longer has the device they used last. The device-loss guidance publishes before the first prompt rather than before the first lockout.

## Support Impact

Access contacts should fall, and the ones left will be harder. A password reset is a procedure support already knows; a lost-device recovery is a judgment call with an identity check behind it. Handle time on access cases will rise even as the count drops, and that should be stated before someone reads the handle-time line as a regression. The first lockout will also arrive before anyone has read the guidance, so support needs its own version of that document on day one.
