---
Name: Dashboard Permission Model
Owner: Erin Vasquez
Status: In Review
Last Updated: 2026-02-09
---

## Problem

Dashboard access is inherited from the folder it sits in. People work around folder permissions by duplicating dashboards into folders they can share, which produces copies that drift, and the copy is often the one that gets circulated.

## Proposal

Permissions on the dashboard itself, with inheritance as a default rather than a mechanism.

- Direct sharing with people and groups, independent of location
- Folder permissions as a default applied at creation, overridable afterwards
- A visible list of who can see a dashboard, including through group membership
- Duplicates detected and surfaced to the author with a link to the original

## Scope

Dashboards. The underlying dataset permissions are a separate and stricter layer and are unchanged.

## Risks

Direct sharing makes it easy to share a dashboard with someone who cannot read its data, producing a broken view rather than a denied one. The sharing flow needs to check data access and say so plainly at the moment of sharing.

## Measurement

Duplicate dashboards created per month, sharing actions using direct permissions, and support contacts about dashboards that render empty.

## Migration

Existing dashboards get a direct permission set derived from their folder, frozen at migration time. From then on, changing the folder's permissions no longer changes theirs, which is the intended behavior and also a silent change for anyone who manages access by editing a folder.

- Derived permissions written for every existing dashboard before the new model goes live
- Folder owners sent a one-time inventory of what detached, rather than discovering it on the next revoke
- Duplicate clusters identified during migration, while the folder structure that explains them still exists

## Interfaces Affected

The who-can-see list has to expand group membership, so the dashboard service starts calling the directory service on a read path it has never touched. Membership changes are not pushed, so the list is only as fresh as the cache behind it. A stale list showing a departed colleague is mildly embarrassing; one that omits someone who can see the dashboard is a real problem, so the cache should fail toward showing more rather than fewer.

## Open Questions

Duplicate detection has no agreed threshold. Two dashboards sharing a dataset and four of six panels are obviously related; two sharing a dataset and one panel are probably not. Nobody has placed that line, and placing it too low turns the prompt into noise authors learn to dismiss, which fails the same way as not having it.
