---
Name: Role Templates for Small Teams
Owner: Tom Okafor
Status: Shipped
Last Updated: 2025-07-08
---

## Context

Our permission model has thirty-one distinct capabilities. Teams under ten people do not want to think about thirty-one of anything, so in practice everyone gets the administrator role and the model does no work.

## Approach

Ship four named templates that cover the realistic shapes of a small team, and keep the full model underneath for those who want it.

- Owner, Editor, Finance, and Viewer, each a named bundle of capabilities
- Templates visible as a starting point, with per-capability editing one click away
- A warning when a workspace has more than three owners, which is the pattern that precedes trouble
- Existing workspaces mapped to the nearest template, with no change in effective access

## Non-goals

No change to the capability set itself, and no new enforcement anywhere.

## Risks

The mapping of existing workspaces had to be exactly access-preserving, because silently expanding or contracting permissions during a migration is the kind of thing that destroys trust in a permission system. We generated the mapping, diffed effective access for every member of every workspace, and only applied where the diff was empty.

## Outcome

Live since June. Administrator-for-everyone dropped from seventy-eight percent of small workspaces to thirty-one, and the owner-count warning has been acted on about half the times it appeared.

## Support Impact

Template names now appear in tickets. Before June a permission question described a capability; it now describes a template, and the responder has to know which capabilities Finance holds before answering. The four bundles went into the support console as a reference card, and the confusion that remains is the gap between a template and an edited template, which look identical in the member list.

- Permission tickets fell by about a fifth, mostly the ones that were really questions about a single checkbox
- A new ticket shape arrived: why a member who is an Editor cannot do one specific thing
- The owner-count warning produces its own small stream of questions about who should be removed

## Prior Art

The capability model came from the enterprise work, where thirty-one capabilities is defensible because a security team is doing the configuring. Three earlier attempts at simplification hid capabilities behind an advanced toggle and failed the same way each time: workspaces found the toggle on day one and never went back. Naming the bundles instead of hiding the detail is the difference, and the drop from seventy-eight percent to thirty-one suggests names were what people were missing.

## Review Notes

Security asked whether a template can drift from its definition after we change a bundle. It can. A workspace keeps the capabilities it was given, so editing the Editor bundle does not change anyone already on it. That was deliberate, because the alternative silently expands access on every workspace, which is exactly what the migration diff existed to prevent.
