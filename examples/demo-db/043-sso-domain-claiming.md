---
Name: SSO Domain Claiming
Owner: Clara Benton
Status: Approved
Last Updated: 2026-05-28
---

## Problem

An organization can enable single sign-on, but existing accounts on their domain keep signing in with passwords. Customers reasonably expect that claiming a domain means everyone on it goes through their identity provider, and today it means nothing of the sort.

## Proposal

Domain claiming with verification and enforced routing.

- Ownership verified by a record in the domain's configuration, re-checked periodically
- Existing accounts on a claimed domain routed to the provider at next sign-in, with their data intact
- A grace period during which both paths work, visible to the organization's administrators
- Personal accounts that happen to use a work address handled through an explicit claim conversation, not silently absorbed

## Scope

Verification and routing. Account merging across domains is a harder problem and is out of scope.

## Risks

The personal account case is genuinely difficult and genuinely important. People have accounts tied to work addresses that contain work they consider theirs, and absorbing those into an organization without consent is both a trust failure and in some jurisdictions a legal one. The claim flow must notify affected users before anything moves.

## Measurement

Domains verified, share of sign-ins on claimed domains going through the provider, and support escalations about absorbed accounts, which we want at zero.

## Rollout

Verification ships first and changes nothing about sign-in: an organization can claim a domain and see the claim confirmed while every account keeps its password. Routing follows, and the first cohort is organizations whose domain carries no personal accounts at all, which the claim flow can determine before anyone is told the feature exists. Only when that cohort is through does routing open up to domains where the hard case actually lives. The grace period starts at thirty days and is not configurable downward in the first release, because the first customer to ask will want it set to zero.

## Failure Modes

- A verification record removed after the initial check, leaving a claim standing on a domain the organization no longer controls; re-checking has to fail slowly enough not to lock out a customer mid-migration
- An identity provider outage while routing is enforced, which locks out an entire domain with no password path left to fall back to
- One person holding both a personal and an organization account on the same address, where routing sends them to a place they did not expect and two histories look like one
- A subdomain claim overlapping a parent domain already claimed by a different organization

## Support Impact

Escalations in this area arrive angry and arrive from someone who believes they have lost their own work. Support needs to see which claim routed a given sign-in and when the affected person was notified, because the first question is always whether they were told. Without that view the case becomes an engineering request, and the person waiting is locked out while it is answered.
