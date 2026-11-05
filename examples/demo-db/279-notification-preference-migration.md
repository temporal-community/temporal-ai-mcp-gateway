---
Name: Notification Preference Migration
Owner: Maya Brennan
Status: Draft
Last Updated: 2025-12-06
---

## Context

Notification preferences are stored in three places: a legacy per-user record, a per-workspace override, and a per-channel setting added last year. The precedence between them is undocumented and, when traced, is not what either the product or support believes it to be.

## Proposal

One preference model with explicit precedence, migrated carefully.

- A single hierarchical model: global, workspace, category, channel, with defined precedence
- Existing preferences migrated to the equivalent effective setting, computed per person
- A migration dry run comparing effective notification behavior before and after, per person
- The old stores removed rather than left synchronized

## Non-goals

No change to anyone's effective preferences through the migration itself. New capabilities come afterwards.

## Risks

A migration that changes someone's effective preferences will either spam a person who had opted out, which is a trust and possibly a legal problem, or silence someone who wanted notifications. The dry run comparison is the gate and no migration should run until its diff is empty or every difference is understood.

## Measurement

Preference records migrated, differences in effective behavior found in the dry run, notification volume per person before and after, and opt-out spikes following migration.

## Sequencing

The dry run is not a step before the migration. It runs continuously for several weeks while the three stores are still live, because preferences keep changing underneath it, and a diff that was empty on Monday says nothing about Friday. The write path moves only once the diff has stayed empty across a full week of normal preference edits.

- Read path computes from both models and compares, recording differences rather than resolving them
- Write path cuts over once the diff holds empty for a week
- Old stores kept readable but no longer written, then dropped a release later

## Rollback

Dropping the old stores is the irreversible step and is deliberately last. Before that point, reverting means pointing the write path back at the three stores, which costs the preference edits made in the new model since cutover. Those are recoverable from the change log but not automatically. After the drop there is no rollback, which is why it waits a release rather than riding along with the cutover.

## Support Impact

Support answers preference questions today by guessing which store won, and they are often wrong, because the real precedence is not the documented one. A single effective setting removes most of that guessing. It also removes their current workaround of setting a preference in whichever store they believe takes priority, so anyone relying on that needs telling before the cutover rather than after.
