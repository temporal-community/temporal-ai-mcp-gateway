---
Name: Abuse Detection on Signups
Owner: Dana Whitfield
Status: In Review
Last Updated: 2026-07-27
---

## Problem

Automated signups create accounts in bursts, consume free tier resources, and are used to send unsolicited invitations from a trusted domain. We detect them after the fact, usually when a recipient complains about the invitations.

## Proposal

Score signups at creation on signals we already have, and restrict rather than block.

- Signals from network reputation, address patterns, and creation velocity per source
- High-scoring signups restricted rather than refused: no outbound invitations until verified
- Verification by a second factor or a short waiting period, not a puzzle
- A review queue for the restricted set, with the restriction lifting automatically on normal behavior

## Non-goals

No challenge puzzle at signup. It penalizes legitimate users measurably and is solved cheaply by the operators we care about.

## Risks

Restricting outbound invitations affects legitimate new workspaces whose first action is inviting their team, which is the behavior we most want to encourage. The verification path has to be fast, and the false positive rate needs measuring on the legitimate population rather than only on the caught abuse.

## Measurement

Automated signups reaching an active state, invitations from restricted accounts, legitimate signups restricted, and time to lift a restriction.

## Data We Have

Six months of labeled abuse exists, but the labels come from complaints, so the population is abuse that sent invitations and annoyed somebody. Quiet abuse that only consumed free tier resources is unlabeled and is probably the larger share. A score tuned against complaint-labeled data will be good at catching the loud kind, which is the kind costing us reputation, and blind to the rest.

- Network reputation and creation velocity are available at signup with no new collection
- Address pattern signals exist, built for another purpose, and need review before reuse
- No labeled set for the quiet population, which bounds what any false negative rate can honestly claim

## Rollout

Score everything and restrict nothing for the first month. Scores are recorded against accounts and then compared with what those accounts did next. An account scored high that went on to invite twelve colleagues and stay active is the false positive this proposal has to price. Restriction turns on at a threshold drawn from that month rather than from an assumption about the shape of the distribution.

## Support Impact

A restricted workspace that cannot invite its team will contact support, and will do it in its first hour, which is the worst possible moment. Support needs to see why an account was restricted and to lift the restriction directly, without an engineer. A restriction nobody can explain and only engineering can remove turns a false positive into a lost customer.
