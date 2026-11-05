---
Name: Deep Link Coverage
Owner: Priya Raman
Status: Approved
Last Updated: 2026-06-08
---

## Background

About a third of our in-product links open the application at its home screen rather than at the referenced content. People sent a link to a specific item land somewhere unrelated and have to search for what they were sent, which defeats the purpose of sending a link.

## Proposal

Complete deep link coverage for every linkable entity, with a verified fallback.

- A link resolver covering every entity type, generated from the routing definition
- Unauthenticated opens route to sign-in and then to the destination, preserving intent
- Links to content the person cannot access show a clear explanation rather than a blank screen
- Automated tests over the full route table on every release

## Scope

The mobile applications. Desktop deep links have the same gap and should follow.

## Risks

Preserving destination through a sign-in flow means holding it somewhere, and that mechanism has historically been where open-redirect problems come from. The destination must be validated against the known route table rather than treated as opaque.

## Measurement

Share of deep links resolving to the referenced content, drop-off between link tap and content view, and time to content when arriving unauthenticated.

## Interfaces Affected

Generating the resolver from the routing definition turns that definition into a contract rather than an implementation detail. A route added without an entity type produces a link that resolves nowhere, so the definition needs a required field and a build-time check that rejects routes missing it. Notification senders are the other affected surface: they build links by string concatenation in three places today, and all three have to call the resolver or the coverage figure will not move for the links people actually tap.

## Failure Modes

- A link tapped on a device without the application installed goes to the store and loses the destination, which no in-application work fixes
- The no-access explanation leaks existence: telling someone an item is not shared with them confirms the item exists, which is right for most entity types and wrong for at least one
- A destination held through sign-in and resumed under a different account sends that person somewhere they should not be

## Timeline

The resolver and the route table tests land in the same release, since the tests are what make a generated resolver trustworthy and neither is worth shipping alone. Sign-in intent preservation follows next, once the route table validation it depends on exists. Desktop keeps its own schedule and starts after the mobile route table has been stable for a full cycle.
