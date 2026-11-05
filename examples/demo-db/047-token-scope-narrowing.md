---
Name: Token Scope Narrowing
Owner: Ruth Adeyemi
Status: Approved
Last Updated: 2026-04-17
---

## Problem

Integration tokens are issued with a scope set that was defined when we had six endpoints. Most integrations hold read and write across everything because that is the only option that reliably works, which makes every integration token a full-access credential.

## Proposal

A finer scope vocabulary, with a migration path that does not break existing integrations.

- Scopes defined per resource and per operation, generated from the interface definition
- Existing tokens mapped to the equivalent broad scopes, unchanged in effect
- New tokens default to the narrowest set that the integration's first calls require
- A report to integration owners showing granted scope against scope actually used

## Non-goals

No forced migration of existing tokens in this phase. The usage report is the persuasion mechanism, and if it is not persuasive we should learn that before mandating anything.

## Risks

Generating scopes from the interface definition means the vocabulary changes when the interface does, which is a versioning problem we have not had to solve before. Scope names become a compatibility surface the moment anyone writes one down.

## Measurement

Share of new tokens issued with narrow scope, median granted-to-used scope ratio across active integrations, and the blast radius of a leaked token, which is the point.

## Prior Art

Our mobile client went through this three years ago, moving from one session token to per-feature scopes, and the lesson was that the usage report changed behavior only once it named a person. Reports addressed to an integration are read by nobody; reports addressed to the engineer who created the token get acted on. Two external platforms we integrate with generate their scope vocabularies the same way, and both froze scope names at first public release and accepted duplicates rather than renaming. That is the cost of generating from an interface definition, paid later.

## Alternatives Considered

Hand-written scopes curated by a small group age better, because a person decides when a new endpoint deserves a new scope and the vocabulary does not churn when the interface is refactored. They were rejected because curation never keeps up. The six-endpoint vocabulary we have now is itself hand-curated work that stopped being maintained, and a generated vocabulary that is occasionally awkward is more honest than a curated one that is quietly stale.

## Open Questions

- Whether a scope name outlives the endpoint it was generated from, which the external precedent says it must
- What the report does with an integration that calls a write endpoint once a quarter, since the granted-to-used ratio will argue against a scope it genuinely needs
- Whether narrow-by-default reaches tokens created by our own first-party clients, which assume full access today
- How an owner asks for a widening without that request becoming a ticket queue
