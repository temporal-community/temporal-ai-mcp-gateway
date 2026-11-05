---
Name: Service Account Key Rotation
Owner: Nikhil Shah
Status: In Review
Last Updated: 2026-02-05
---

## Background

Service account keys do not expire. The oldest live key in production was issued in the first year of the company, and nobody currently employed knows what uses it. Our own security review has flagged this for three cycles running.

## Proposal

Introduce expiry, rotation tooling, and usage visibility, in that order of importance.

- Every key gets a last-used timestamp and a calling-service attribution
- New keys expire after one year by default
- Overlapping rotation supported, so a service can hold two valid keys during a change
- Keys unused for ninety days are disabled after notification, with a self-serve restore

## Non-goals

No immediate expiry for existing keys. Visibility first, then a deprecation schedule agreed with each owning team.

## Risks

Disabling an unused key disables whatever uses it once a year, which is exactly the integration nobody remembers until it fails at quarter end. The notification period must be long and the restore path must be fast, and we should expect to be wrong about at least one key.

## Measurement

Share of live keys with known attribution, age of the oldest live key, and keys rotated without an incident during the change.

## Sequencing

Attribution lands well before expiry, with a gap wide enough to feel slow. A last-used timestamp costs nothing to add and answers the only question anyone has about the oldest key; expiry without attribution is a scheduled outage with better paperwork. A full quarter of usage data is also the minimum that separates a key used once a year from a key used never, and nothing shorter can tell those apart.

## Interfaces Affected

- Key issuance, which gains an expiry field and a default that every existing caller inherits without asking for it
- The credential store, which has to hold two valid keys for one service through an overlap window
- Deploy configuration for services that read a key once at start-up, since those will not pick up a rotation without a restart
- The security review document, which has carried this finding for three cycles and is where progress should be recorded

## Open Questions

Who owns a key whose attributed calling service has itself been decommissioned, which probably describes several of the oldest ones. Also whether ninety days is the right threshold at all: the failure this proposal is most worried about is the integration that runs once a year, and a disable threshold shorter than that period guarantees we break it rather than merely risking it.
