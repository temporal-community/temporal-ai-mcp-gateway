---
Name: Referral Program Mechanics
Owner: Nikhil Shah
Status: Parked
Last Updated: 2026-01-18
---

## Context

About a quarter of self-serve signups cite a colleague or friend as how they heard about us. We have no referral mechanism, so this happens entirely outside anything we can see or support.

## Proposal

A simple two-sided referral with credit rather than cash.

- A referral link per account, with attribution on signup
- Credit to both parties, applied to the next invoice, with a cap per account per year
- Fraud controls on self-referral and on disposable addresses
- A visible referral state so the referrer knows what happened

## Scope

Self-serve accounts. Referrals into enterprise deals are a partner conversation with different economics.

## Risks

Referral programs attract exactly the behavior the fraud controls are meant to stop, and the controls are never finished. More fundamentally, adding an incentive to a thing people already do voluntarily can crowd out the voluntary behavior, which would be a net loss that our measurement would struggle to detect.

Parked pending a view on whether the incentive is necessary at all, which is a question for the growth team rather than for engineering.

## Measurement

If it proceeds: referred signups as a share of total, conversion rate of referred accounts, credit issued, and the volume of attempted abuse.

## Data We Have

The quarter figure comes from the optional free-text field at signup, coded by hand once last autumn. It is weak in both directions: about a third skip the field, and a colleague mentioning us is not a colleague advocating for us. Nothing in the data separates a referral worth paying for from an offhand recommendation.

- No link between a citing signup and the account cited, so referral chains are invisible
- Conversion of signups citing a person runs four points above the self-serve average
- Disposable address detection already exists in the signup path and would be reused

## Alternatives Considered

A one-sided reward to the referrer alone is cheaper and easier to reason about, and it gives the referred person nothing at the moment they are deciding. A non-monetary acknowledgement, naming the referrer in the new workspace, avoids the crowding-out risk entirely but has no evidence behind it and would be hard to tell apart from doing nothing.

## What Would Change Our Mind

Unparking should follow evidence about the voluntary behavior rather than a decision to try the program and watch. A cohort comparison across two quarters, between accounts that arrived through a cited colleague and the rest, would say whether that path is already strong enough to leave alone. If it is, the incentive is a cost carrying a downside and no upside.
