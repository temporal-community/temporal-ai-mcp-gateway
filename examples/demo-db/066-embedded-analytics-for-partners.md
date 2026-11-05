---
Name: Embedded Analytics for Partners
Owner: Hugo Takahashi
Status: Draft
Last Updated: 2025-10-28
---

## Context

Partners want to show our analytics inside their own products. Today they call the reporting interface and rebuild the charts, which is slow for them, inconsistent for their users, and produces support questions that reach us without any context.

## Proposal

An embeddable view with scoped credentials and a constrained theme.

- Signed embed tokens scoped to a single account and a single dashboard
- Theme variables for color and typography, with layout fixed
- No navigation out of the embed, and no access to underlying data beyond the rendered view
- A documented versioning policy so partners are not surprised by changes

## Scope

Four dashboards chosen with the partner team. An embed surface is a long-term commitment and should start narrow.

## Risks

Embedding makes our rendering a dependency of someone else's product, which means their incidents become ours and our changes become theirs. The versioning policy is the whole safety mechanism and needs to be conservative in a way that will feel slow internally.

## Measurement

Partners embedding, embed views per week, support contacts routed through partners, and the number of breaking changes we need to make in the first year.

## Operational Impact

An embed makes our availability visible inside a product we do not control, and a partner's user cannot tell whose outage they are looking at. A failing embed has to say that our view is unavailable rather than render blank, because a blank panel in someone else's product gets attributed to them and reaches us late.

- Embed traffic needs its own error budget, separate from the main product's
- The four dashboards become change-controlled surfaces with their own review
- Token issuance and revocation have to be auditable per partner

## Support Impact

Questions will arrive second-hand, from a partner relaying a user they cannot see. The embed should carry a view reference the partner can pass on, so a question arrives with the dashboard, the account scope, and the render time attached. Without it, each one starts with three rounds of reconstruction through an intermediary, which is worse than today, where at least the customer is in the room.

## Timeline

The versioning policy is written and agreed before the first partner is given a token, not after the first breaking change. It is the cheapest thing on this list and the one that becomes impossible to introduce later: a policy added once partners have shipped is a negotiation rather than a decision.
