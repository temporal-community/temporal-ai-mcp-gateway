---
Name: Certificate Renewal Automation
Owner: Ben Tsai
Status: Shipped
Last Updated: 2025-08-18
---

## Background

Certificates were renewed by hand against a calendar reminder. We had two expiry incidents in three years, both on certificates that were not on anyone's calendar because the person who created them had left.

## Approach

Automatic issuance and renewal, with discovery to find what we did not know about.

- Automated issuance for every certificate the platform terminates
- A scanner across our address space finding certificates we do not manage
- Renewal at two-thirds of lifetime, with alerting if renewal fails rather than if expiry approaches
- An inventory with owner and renewal state, generated rather than maintained

## Non-goals

No change to the certificates customers install for their own domains, which is a separate flow with a separate problem.

## Risks

The scanner finds certificates in places nobody expected, and some of those are on systems where automated renewal is not possible. The inventory has to distinguish managed from merely known, or the green state will be misleading.

## Outcome

Shipped in July. The scanner found nineteen certificates outside the managed set, of which eleven have since been brought in and six were on systems that have been decommissioned. No expiry incidents since.

## Prior Art

The calendar reminder was itself the fix for an earlier expiry, and it held for exactly as long as the person who owned the entry stayed. That is the pattern: every previous attempt here depended on somebody remembering, and the failure was always departure rather than carelessness. Alerting on renewal failure instead of on approaching expiry follows from the same observation. An expiry alert announces that something will break and hands you the work; a renewal-failure alert says something already went wrong while a third of the certificate's lifetime is still left to fix it in.

## Operational Impact

Certificate work moved off the calendar and onto the alert rotation, at roughly two alerts a month, almost all of them a validation record that moved or a host the scanner found and cannot renew for. The inventory is generated so nobody maintains it, but the merely-known entries still need a human to triage them, and three of the nineteen have sat in that state for months. That is the honest reading of the dashboard being green.

## Open Questions

What to do with the hosts where automated renewal is not possible: accept a documented manual process with a named owner, or decommission them the way the other six went. Nobody has owned that decision since the list got short enough to ignore. The customer-domain flow named as a non-goal also has the same discovery gap, and nothing here has made that better.
