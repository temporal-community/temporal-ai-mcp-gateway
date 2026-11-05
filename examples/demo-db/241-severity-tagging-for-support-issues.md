---
Name: Severity Tagging for Support Issues
Owner: Tom Okafor
Status: Draft
Last Updated: 2025-09-15
---

## Background

Support uses its own severity scale, engineering uses another, and the two do not map. A customer-blocking issue tagged urgent in support arrives in engineering as an ordinary item, which is why several urgent issues have waited a week.

## Proposal

One scale across both, defined by customer impact rather than by internal urgency.

- A shared four-level scale with worked examples from both sides
- Support's tag carried through escalation rather than retranslated
- Disagreement resolved by a named person rather than by whoever argues longer
- Weekly review of the highest level, which should be rare enough to review individually

## Scope

Customer-reported issues. Internal incidents use the incident severity definitions, which this should align with but not duplicate.

## Risks

A shared scale means support can set engineering's priorities, which engineering will resist, reasonably, since support sees individual cases rather than aggregate impact. The named resolver is the mechanism that makes this workable and the role needs genuine authority rather than being a nominal tiebreaker.

## Measurement

Time from report to engineering acknowledgement by severity, disagreements raised, and issues escalated twice because the first attempt was downgraded.

## Migration

Several hundred open issues carry one of the two old tags, and retagging them by hand is not worth it. They map mechanically to the nearest new level and are retagged on next touch rather than in a sweep. Anything already at the top of either scale gets reviewed individually, since those are where a wrong mapping costs something. Closed issues keep their original tags, so severity trends cannot be compared across the cutover and the first report will show a step change we should explain.

## Staffing

The named resolver is a new role and the proposal does not say whose. It needs someone who sees both aggregate engineering load and individual customer impact, which means a support lead and an engineering lead in turns, or one person sitting across both. Appointing the wrong person is worse than leaving the role empty: a resolver without authority turns every disagreement into a longer argument with an extra step.

- The resolver is named before the scale is published, not after the first dispute
- Top-level issues reviewed weekly by the resolver and the on-call engineering lead together
- Worked examples maintained by the resolver, since they are the real definition

## Review Notes

Both existing scales have definitions that sound clear and are applied inconsistently, which suggests definitions are not what fixes this. Ten real past issues placed on the scale by both teams, with the disagreements left visible, would be a better artifact than another definition paragraph.
