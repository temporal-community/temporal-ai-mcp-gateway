---
Name: Cross-Workspace Search Boundaries
Owner: Nikhil Shah
Status: In Review
Last Updated: 2026-04-26
---

## Problem

People who belong to several workspaces search within one at a time and switch to look in another. The common case, finding something when you cannot remember which workspace it was in, requires searching each in turn.

## Proposal

Search across the person's own workspaces, with strict scoping and clear attribution.

- Results from every workspace the person is a member of, grouped by workspace
- Permissions evaluated per result at query time, never cached across workspaces
- The workspace shown prominently on each result, since the same title can exist in several
- An explicit setting for organizations that require search to stay within their boundary

## Scope

Search for individuals across their own memberships. No change to what any workspace can see of another.

## Risks

This is a permission boundary crossing, and a bug here leaks one organization's content to another. Permission evaluation must happen per result at query time even though caching would be faster, and this should be stated as a non-negotiable design constraint rather than a preference. The organizational opt-out exists because some customers will require it contractually.

## Measurement

Cross-workspace searches run, results opened from a workspace other than the current one, organizations enabling the restriction, and any permission defect found in review or testing.

## Interfaces Affected

The search API gains a scope parameter and loses the assumption that one request belongs to one workspace, which several callers rely on today.

- The search endpoint, where the workspace identifier moves from request context onto each result
- The index selector, which resolves one shard set per request today and now resolves several
- Organization settings, which gain the restriction toggle and have to say plainly what it turns off
- Audit logging, which records a search against a workspace and now needs one record per workspace touched

## Cost

A query that hit one index now hits as many as the person has memberships, and the median multi-workspace member belongs to three. Per-result permission evaluation is the other half: it cannot be cached across workspaces, so cost scales with results returned rather than with queries run. Capping the per-workspace result set before evaluation keeps that bounded, at the price of a workspace occasionally being underrepresented in the blended list.

## Review Notes

Security had one addition: the organizational restriction has to be evaluated on the serving path rather than applied as a filter over assembled results, because a filter applied late is one a new code path can forget. Legal asked whether the setting belongs to the organization or to the workspace, since an organization running several workspaces may want the boundary drawn around all of them, and that is still open.
