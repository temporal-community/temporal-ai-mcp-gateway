---
Name: Incident Disclosure Policy
Owner: Priya Raman
Status: In Review
Last Updated: 2026-02-18
---

## Problem

When a security incident affects customers, what we tell them and when is decided case by case, under pressure, by whoever is in the room. Our last two disclosures were inconsistent in tone, detail, and timing, which customers compared and noticed.

## Proposal

A written policy agreed in advance, covering thresholds, timing, and content.

- Disclosure thresholds defined by data category and affected population
- Timing commitments measured from confirmation rather than from discovery, stated plainly
- A template covering what happened, what data was involved, what we did, and what the customer should do
- Named roles for approval, so the decision path is known before it is needed

## Scope

Security incidents affecting customer data. Availability incidents follow the status page process.

## Risks

A policy with timing commitments will at some point require disclosing before the investigation is complete, which means disclosing something that later turns out to be partly wrong. That is the correct trade and it needs to be understood in advance, including by the people who will be uncomfortable with it in the moment.

## Measurement

Disclosures made within the committed timing, consistency against the template, customer contacts following a disclosure, and regulatory notifications made within statutory deadlines.

## Dependencies

Thresholds defined by data category depend on a categorization this policy does not own. The category labels have to exist on the stores an incident would touch before a threshold written in those terms can be applied. Legal has to confirm that a commitment measured from confirmation does not weaken a statutory deadline measured from discovery, since the two clocks differ and the stricter one governs. The template also needs a delivery path that reaches account administrators rather than billing contacts, which is the list we have today.

## Prior Art

The last two disclosures are both the evidence for this proposal and the best test available of it. One went out in nine hours, ran to three paragraphs, and told the customer nothing to do. The other took six days, ran to two pages, and named internal systems the reader had no way to recognize. Running both backwards through the proposed thresholds and template is the cheapest check we have, and it belongs before approval rather than after.

## Open Questions

Who may start the disclosure clock. Confirmation is a judgment, and if the on-call responder can make it the clock starts in the first hour, while if it waits for a named approver it starts when that person is awake. We have also not settled whether a disclosure that later proves partly wrong is corrected by updating the original notice or by sending a second one, and the answer changes what the first notice is allowed to promise.
