---
Name: Magic Link Expiry Policy
Owner: Yusuf Demir
Status: Draft
Last Updated: 2025-08-14
---

## Context

Sign-in links are valid for twenty-four hours and can be used more than once. That was a deliberate choice to reduce support load when links were new, and it is now the weakest part of the sign-in surface: a forwarded email is a valid credential for a day.

## Proposal

Shorten the window, make links single-use, and bind them to the requesting context.

- Fifteen-minute validity, single use, invalidated on first successful consumption
- Bound to the browser that requested it, with a clear message and an easy resend when opened elsewhere
- Rate limits per address and per network on both request and consumption
- Expired links land on a page that resends rather than a dead end

## Non-goals

No change to passkey or password sign-in, and no change to the invitation flow, which has a different threat model and a legitimate need for long-lived links.

## Risks

Browser binding breaks the common and entirely reasonable habit of requesting on a laptop and opening on a phone. The resend path has to be good enough that this is a minor annoyance rather than a reason to give up, and we should measure abandonment at that step specifically.

## Measurement

Sign-in completion rate through the link path, resends per successful sign-in, and reports of unauthorized access attributed to forwarded mail.

## Rollout

Shortening the window and making links single use go out together, since both are server-side and neither depends on the resend page being good. Browser binding waits for that page, because binding without a smooth resend turns the laptop-to-phone habit into a dead end. Rate limits land last and are tuned against observed request rates rather than a chosen number, since a limit set too low locks out a shared office before anyone reads the alarm.

## Failure Modes

- A mail client that prefetches links, consuming a single-use link before the person clicks it
- A link opened in the mail application's embedded browser, which is not the requesting browser and fails binding for a reason nobody can see
- Fifteen minutes expiring inside a delivery delay, so the link is dead on arrival and the resend produces another dead one
- Rate limits treating a corporate network as one requester, so one person's retries block a colleague

Prefetching is the one that breaks sign-in quietly for an entire mail provider, so consumption has to require a request from a browser rather than any fetch of the link.

## Review Notes

Security asked for five minutes and settled on fifteen against delivery evidence: our own send-to-open data has a tail well beyond five minutes that is not ours to fix. The invitation flow was carved out again in review, since an invitation goes to someone who has no account yet and cannot resend it to themselves.
