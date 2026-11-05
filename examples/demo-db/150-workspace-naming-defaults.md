---
Name: Workspace Naming Defaults
Owner: Ines Duarte
Status: Shipped
Last Updated: 2025-06-27
---

## Background

Workspace name was a required free-text field at creation with no default. A surprising share of workspaces ended up called untitled, test, or the person's own name, which becomes awkward once colleagues join and is rarely corrected afterwards.

## Approach

Suggest a sensible default and make renaming obvious later.

- Default derived from the address domain for work addresses, left blank otherwise
- The field editable at creation, not locked to the suggestion
- A rename prompt when the second member joins, which is the moment the name starts to matter
- Rename available from the workspace header rather than only in settings

## Non-goals

No enforcement of naming conventions, which would be both annoying and ineffective.

## Risks

Deriving a name from a domain exposes that we know the company name, which in testing nobody found objectionable but which we checked rather than assumed.

## Outcome

Shipped in May. Workspaces named test or untitled fell from about nine percent of new creations to under one, and the rename prompt at second member is acted on roughly a third of the time.

## Support Impact

Renaming used to be a ticket, because the control lived in settings and settings is where people look last. Moving it into the header removed most of those. What remains is the case a rename does not solve: the workspace address does not change with the name, so someone who renamed to fix a typo is still sharing the old link.

- The header control is now the first thing a responder points at
- Address and name being separate belongs in the rename interface, not in a help article
- Workspaces created before May keep whatever they were called, which is most of the remaining complaints

## Interfaces Affected

- Workspace creation, where the suggestion renders and stays editable
- The invitation path, which is what triggers the second-member prompt
- The workspace header, which gained an inline rename
- Address derivation, already domain-aware and unchanged, which is part of why this shipped quickly

## Open Questions

- Whether the second-member prompt should repeat at a later threshold, since two thirds ignore it first time
- What a workspace on a personal address should default to, which is still blank and still ends up as a person's name
- Whether the historical population is worth prompting, given members have read the bad name as normal for long enough
