---
Name: Third-Party Risk Questionnaire
Owner: Nora Sellers
Status: Draft
Last Updated: 2026-03-23
---

## Context

Every new vendor is assessed with a questionnaire that takes the vendor two weeks to complete and our security team two hours to read. The questions were assembled from three templates, several overlap, and the answers rarely change a purchasing decision.

## Proposal

Tier the assessment by what the vendor actually touches.

- Three tiers by data access and system access, assessed at intake
- The lowest tier satisfied by an existing certification rather than a questionnaire
- The highest tier keeping the full assessment plus evidence review
- Reassessment on a cycle proportional to tier rather than annually for everyone

## Non-goals

No change to contractual security terms, which are owned by legal.

## Risks

Tiering at intake depends on an accurate description of what the vendor will access, which is given by the person who wants to buy the tool and who has an incentive to describe it narrowly. A check at the point of access provisioning is what catches the mismatch, and without it the tiering is self-certified.

## Measurement

Time from vendor selection to approval by tier, assessments completed, mismatches found at provisioning, and vendor-related security incidents.

## Dependencies

Tiering at intake needs the intake form to ask what the vendor will access before a tier can be assigned, and the current form asks only for a business justification and a budget code. The provisioning check named in Risks depends on access grants being visible to the security team, which today is true for the identity provider and the cloud accounts but not for vendor-managed portals that issue their own logins.

- Intake form gains two access questions, owned by procurement
- Certification acceptance list maintained by the security team, reviewed quarterly
- Provisioning events from the identity provider exported to the assessment record

## Rollout

The three tiers go live for new vendors first, with the existing vendor population left on its annual cycle until each one's next renewal date. Reassessing the whole population at once to place it in tiers would cost more than the change saves in its first year, so placement happens at renewal and the mixed state lasts twelve months.

## Open Questions

Whether a vendor that declines to share evidence for the highest tier is rejected outright or escalated to a named approver is undecided, and the two produce different relationships with the business units that want the tool. It is also unsettled who re-tiers a vendor whose access expands after approval, since the expansion is usually requested by the business unit rather than reported by the vendor.
