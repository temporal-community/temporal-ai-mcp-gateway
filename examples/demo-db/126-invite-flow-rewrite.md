---
Name: Invite Flow Rewrite
Owner: Marcus Reyes
Status: In Review
Last Updated: 2026-07-09
---

## Problem

Inviting a colleague requires leaving the current context, opening settings, finding the member list, and typing an address. Workspaces that stay single-person churn at four times the rate of those that reach two, and our invite rate in the first week is eleven percent.

## Proposal

Make inviting possible from where the need arises.

- An invite control wherever sharing or assignment implies another person
- Address entry with suggestions from the organization directory when one is connected
- A copyable link as an alternative, scoped and expiring
- The invited person landing directly in the context they were invited to, not on a generic home screen

## Scope

Invitation into an existing workspace. Creating a new workspace with a team is a different flow and keeps its current design.

## Risks

Making invitation easy makes mistaken invitation easy, and an invitation to the wrong address exposes the workspace name and the inviter's identity at minimum. A short undo window and a clear pending state cover most of this; nothing covers all of it.

## Measurement

Invites sent per new workspace in week one, workspaces reaching two active members, and invitations revoked within an hour, which is the error signal.

## Interfaces Affected

The invite control turns up in more places than the member list ever did, and each one has to carry the same pending state and the same undo.

- Share and assignment surfaces, where the control is new
- The member list, which stops being the entry point and becomes where pending invitations are managed
- The invitation message, which now carries the destination context instead of a generic link
- The directory connection, which gains a suggestion path and the access question that comes with it

## Failure Modes

A mistyped address that happens to match a real account elsewhere, accepted before the undo window closes. A link pasted into a shared channel, which is scoped and expiring and still wider than anyone intended. And a directory suggestion offering someone who left the company, since directory freshness is the other side's problem and surfaces as our mistake.

## Rollout

Assignment first, sharing second, because assignment names a specific person and the suggestion list is doing less of the work. The copyable link ships only once the pending state and the undo are in place on both, since it is the control with the widest reach and the least feedback. Revocations within an hour are measured from the first surface rather than waited for across all of them.
