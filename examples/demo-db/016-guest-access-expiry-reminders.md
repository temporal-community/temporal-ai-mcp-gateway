---
Name: Guest Access Expiry Reminders
Owner: Grace Lindqvist
Status: Shipped
Last Updated: 2025-06-30
---

## Context

Guests invited into a workspace stay forever. Workspaces that have been running for more than two years typically have more guests than members, and most of those guests are from companies the customer no longer works with.

## Approach

An expiry date on guest access, with reminders rather than silent removal.

- Default ninety-day expiry on new guest invitations, adjustable at invitation time
- Reminders to the inviting member at fourteen days and at expiry
- Extension in one click from the reminder
- Existing guests given an expiry date set well out, with a workspace-level review prompt

## Non-goals

No automatic removal of existing guests, which would break live work for the sake of tidiness.

## Risks

The reminder goes to the inviting member, who may have left. The fallback is the workspace administrator, and where there is no active administrator the guest keeps access and the workspace appears in an internal report. Removing access from an unattended workspace is not something we should do automatically.

## Outcome

Shipped in May. Guest count per workspace is down about a fifth across workspaces older than two years, and roughly sixty percent of reminders result in an explicit extension, which suggests the access was still wanted and now has an owner.

## Support Impact

Two contact types appeared that did not exist before. The first is a guest who lost access and does not know why; support points them back at the member who invited them rather than restoring access, since support cannot judge whether the expiry was correct. The second is a member asking why a reminder arrived for a guest they do not remember inviting, which is nearly always an invitation issued on a colleague's behalf two years earlier. Neither is frequent, and both arrive with no context attached.

## Failure Modes

- One-click extension from the reminder can be granted by whoever opens the mail on a shared device, which is why the click requires an active session and not a signed link alone
- A guest invited by someone who has left, in a workspace with no active administrator, keeps access indefinitely by design, and the internal report listing those workspaces only helps if somebody reads it
- Invitations issued in bulk expire in bulk, producing one reminder naming thirty guests, which reads as noise rather than as a decision

## Open Questions

Ninety days was chosen because it is a quarter, not because anything measured it. The sixty percent extension rate fits a default that is too short and fits equally a default that is about right with genuinely ongoing access. Nothing collected so far separates the two.
