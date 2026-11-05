---
Name: Backup Restore Verification
Owner: Caleb Mortensen
Status: Approved
Last Updated: 2026-05-25
---

## Context

We take backups and monitor that they complete. We do not restore them. The last verified restore was during the migration two years ago, and the backup format has changed since.

## Proposal

Automated restore verification on a schedule, into an isolated environment.

- Weekly restore of the primary datastores into an isolated environment
- Verification beyond completion: row counts, referential checks, and a sample of business-level assertions
- Time to restore measured and compared against the stated recovery objective
- Failure of a verification treated as an incident, because that is what it is

## Scope

The four datastores whose loss would stop the product. Others are verified quarterly.

## Risks

Restoring into an isolated environment proves the backup is readable, not that the restore procedure works under incident conditions with the real network, real secrets, and a person who has not done it before. The quarterly drill should include at least one restore performed by someone following the documentation rather than by the automation.

## Measurement

Restores verified per month, time to restore against objective, verification failures, and whether the documented procedure survives being followed by someone unfamiliar with it.

## Cost

A weekly restore of four datastores is compute for the duration plus storage for the restored copy until teardown. The largest restores in roughly five hours, so that environment exists for most of a day each week.

- Restore compute sized for speed rather than price, since time to restore is itself one of the measurements
- Storage held only until verification completes, with teardown automatic rather than scheduled
- Business-level assertions written once per datastore and maintained with the schema, the recurring cost nobody counts

## Failure Modes

The quiet failure is a verification that passes on a backup taken from a replica that was itself behind. The data is internally consistent, the row counts look plausible against a lagging source, and nothing says the backup is older than it claims. Comparing the restored high-water mark against production at backup time catches it. The second is assertion rot: assertions written against today's schema fail for the wrong reason after a migration, and a verification failing every week post-migration gets muted rather than fixed, so assertion maintenance belongs in the migration.

## Timeline

Four weeks to the first automated restore of the largest datastore, which is the one worth knowing about. The other three follow over the month after. The quarterly drill with a person following the documentation is scheduled from the start rather than added later, since the documentation gap is what an actual incident would otherwise find.
