---
Name: Mention Notifications Scoping
Owner: Lena Fischer
Status: In Review
Last Updated: 2026-05-04
---

## Context

Mentioning a group notifies everyone in it immediately, with no indication to the sender of how many people that is. In our largest workspaces a single mention has notified over four hundred people, and the pattern repeats weekly.

## Proposal

Make the cost of a broad mention visible and give recipients control.

- A confirmation when a mention would notify more than a threshold, stating the number
- Per-group notification preference for recipients, including digest rather than immediate
- Large-group mentions restricted to workspace roles that should have that reach
- A record of broad mentions, so the pattern is visible to workspace administrators

## Non-goals

No change to direct personal mentions, which are the mechanism working as intended.

## Risks

Restricting who may mention a large group puts a permission between someone and an announcement they legitimately need to make, and the first time it blocks something urgent it will be remembered. The confirmation should carry most of the weight, with restriction reserved for the largest groups.

## Measurement

Broad mentions per workspace per week, confirmations shown and abandoned, notification disable rate in large workspaces, and complaints about mention noise.

## Rollout

Confirmation first, everywhere, with the threshold high enough that only genuinely broad mentions trigger it. Three or four weeks of that says how many broad mentions are deliberate: an author who sees the number and sends anyway has chosen, and one who abandons had not understood the reach. Restriction follows, and only for the group sizes where the abandon rate shows people are surprised by their own reach.

- Confirmation live at a high threshold, abandon rate recorded
- Recipient preference per group, digest included
- Restriction by role, largest groups only, once that data exists

## Interfaces Affected

Counting recipients before the mention is sent is new work in the composer, and the count is not the group's membership: it excludes people already viewing the item, people whose preference is digest, and anyone whose access was revoked while their group membership was not. A confirmation that overstates the number teaches people to dismiss it, so the figure shown has to be the number actually notified.

## Open Questions

The digest preference has no agreed schedule. A daily digest is useless for an announcement about today, and a four-hour one is close enough to immediate that it does not reduce noise. Whether an administrator can set a default preference for a group, or only individuals can, is also undecided, and it matters most in exactly the large workspaces this targets.
