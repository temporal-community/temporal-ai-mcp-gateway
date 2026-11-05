---
Name: Incident Tooling Consolidation
Owner: Nora Sellers
Status: Draft
Last Updated: 2025-08-25
---

## Problem

During an incident we use a paging tool, a chat channel created by hand, a status page updated separately, a document for the timeline, and a tracker for the follow-ups. Keeping them in sync is work done by the person who can least afford it, which is the incident lead.

## Proposal

One command that creates the whole incident context, with state flowing between the pieces.

- Declaration creating the channel, the document, the status page entry, and the tracker item
- Severity and status changed in one place and propagated
- The timeline assembled from the channel rather than typed separately
- Resolution closing everything and producing the postmortem skeleton

## Scope

Incident coordination. Alerting and paging are unchanged.

## Risks

A tool that creates five things creates five things to clean up when an incident is declared in error, which happens and should remain cheap. Undeclaring needs to be as easy as declaring, or people will hesitate to declare, which is the behavior we least want.

## Measurement

Time from declaration to coordinated context, status page updates made during incidents, and incident lead feedback on coordination overhead.

## Rollout

For the first month the command creates only the channel and the timeline document, the two artifacts every incident has and the two with no external audience. The status page entry joins after a decision about who may publish one, since today that is four named people and this would quietly widen it to anyone able to declare. Tracker items go last, because follow-ups created automatically and never groomed are how the tracker lost its credibility the first time.

## Failure Modes

- A partial create, where the channel exists and the status page entry does not, and the lead never notices because the command reported success
- Timeline assembly sweeping in the channel's side conversations, yielding a document nobody reads and a postmortem that starts from noise
- Severity changed in the tool while a different severity is announced in the channel, so the propagated value and the spoken one diverge mid-incident
- A declaration attempted while the tool itself is part of the outage, which is exactly when it is most wanted

## Staffing

One engineer for roughly two months covers the command and the state propagation. The schedule risk is not the code: four of the five systems are owned by different teams, and two of them rate-limit the kind of automated creation this needs. Those conversations should start before the work does, because they will take longer than the implementation and nothing about them is visible on a burndown.
