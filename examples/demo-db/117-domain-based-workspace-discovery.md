---
Name: Domain-Based Workspace Discovery
Owner: Jonas Keller
Status: Draft
Last Updated: 2025-09-16
---

## Context

People signing up with a work address frequently create a new workspace when their colleagues already have one. We then have two workspaces for one company, with content split between them, and the merge request arrives three months later.

## Proposal

Offer to join an existing workspace when the address domain matches one.

- At signup, matching domains surfaced as a suggestion to request access
- The request routed to the workspace administrators, never granting access automatically
- Workspace administrators able to disable discovery for their domain
- Common free address domains excluded entirely

## Scope

Signup. Discovery from within the product, for people who already have an account, is a later step.

## Risks

Revealing that a workspace exists for a domain is a small information disclosure, and for a company that has not announced a tool choice it could be unwelcome. Allowing administrators to disable it covers the stated case; the default is the question, and the proposal is to default to on for paid workspaces only.

## Measurement

Join requests raised and approved, duplicate workspaces per domain, and merge requests received, which is the cost we are trying to avoid.

## Prior Art

Domain capture is a well-worn pattern, and the variations matter more than the idea. Some products auto-join anyone whose address domain matches, which removes the request step and the administrator's control with it; that is the version the risks section rules out. Others require a DNS record before discovery turns on, which is strict, slow, and the reason uptake of it is low. This proposal sits between the two: matching is advisory, joining requires approval, and verification is not a prerequisite for being suggested.

## Cost

A small build with ongoing maintenance in the exclusion list.

- Domain matching and the request route are a few weeks of work on the signup path
- The free-domain exclusion list needs a source and a refresh schedule, since a stale list leaks suggestions
- Administrator request queues add a support surface when nobody approves and the requester contacts us instead

## Open Questions

Whether an unanswered join request should expire or keep the person waiting. Expiring it sends them to create their own workspace, which is the outcome this exists to prevent; leaving it open strands them. We have also not settled the case of a domain with several workspaces, where the suggestion becomes a list and the person has to choose between workspaces none of whose contents they can see.
