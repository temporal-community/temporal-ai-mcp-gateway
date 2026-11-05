---
Name: Bug Bounty Payout Policy
Owner: Clara Benton
Status: Parked
Last Updated: 2026-01-31
---

## Context

The disclosure program will bring researchers. Some of them will ask what we pay, and the answer today is nothing, which is a legitimate position and one we should state deliberately rather than by omission.

## Proposal

A published reward table tied to severity and impact, with a bounded annual budget.

- A table by severity with ranges rather than fixed amounts, since impact varies
- Duplicates and known issues excluded explicitly, with the definition of known published
- An annual budget with a stated behavior when exhausted, rather than silent refusal
- Payment handled through a platform rather than directly, for the tax and sanctions handling

## Scope

Rewards for the disclosure program, if it proceeds.

## Risks

Paying for vulnerabilities attracts volume, most of it low quality, and the triage cost reliably exceeds the payouts. We should not start this until the disclosure program has run for two quarters and we know our triage capacity. Parked for that reason rather than on principle.

## Measurement

If it proceeds: valid reports per quarter, cost per valid report including triage time, severity distribution, and whether the reports found anything our own testing did not.

## Alternatives Considered

- Recognition without payment: a published acknowledgements page and a committed response time, which costs no budget and still attracts researchers who work for reputation
- Invitation-only rewards, extended after the disclosure program identifies people who send good reports, which bounds the volume problem and is plainly less fair
- Paying only in the severity bands our own testing struggles to reach, which is honest about why we would pay at all and looks arbitrary from outside

## Staffing

Triage is the cost here, not the rewards. Every report needs someone who can reproduce it, judge severity, and answer within the stated time, and that lands on a security team whose size was set before any of this existed. The two quarters of disclosure data should give a reports-per-week number; multiplying it by an honest triage hour and comparing that against the proposed budget is a more useful conversation than arguing about the top of the reward range.

## What Would Change Our Mind

If the first two quarters bring few reports and most duplicate findings we already had, there is no case for paying: the budget would buy volume we cannot triage and results we already own. The opposite outcome is the one that would move this from optional to urgent — reports reaching things our own testing does not, sent by people who asked about rewards before deciding whether to keep looking.
