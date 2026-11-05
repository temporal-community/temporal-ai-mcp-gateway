---
Name: Encryption Key Management
Owner: Tom Okafor
Status: Draft
Last Updated: 2026-06-02
---

## Background

Data at rest is encrypted with keys managed by the cloud provider's default service, with one key per datastore and no rotation. This satisfies most questionnaires and gives us little actual control, including no ability to offer customer-managed keys, which three enterprise prospects have asked for.

## Proposal

A deliberate key hierarchy with rotation, and a path to customer-managed keys.

- A key hierarchy with per-workspace data keys wrapped by a regional master key
- Automatic rotation of data keys, with re-wrapping rather than re-encryption
- Customer-managed master keys as an enterprise option, including the ability to revoke
- Key operations logged separately with their own retention and access controls

## Scope

Data at rest in the primary datastores. Backups inherit the hierarchy and need their own handling for revocation.

## Risks

Customer-managed keys mean a customer can render their own data unreadable, deliberately or by accident, and recovery is impossible by design. That consequence must be understood by the customer before the option is enabled, in writing, and our own operational procedures must handle the revoked state gracefully rather than as an outage.

## Measurement

Keys rotated on schedule, enterprise deals where customer-managed keys were required, time to revoke, and key operation audit coverage.

## Migration

Existing data sits under provider-managed keys with nothing beneath them, so the hierarchy has to arrive without a re-encryption pass over everything at once.

- New writes take a per-workspace data key from the day the hierarchy exists
- Existing data is re-keyed workspace by workspace in the background, with the old key kept until that workspace finishes
- A workspace becomes eligible for a customer-managed master key only once it is fully re-keyed, since a partial state cannot be revoked cleanly
- Backups written before the cutover stay readable under the old key for their retention period

## Operational Impact

Key operations become a dependency on the read path, which they effectively are not today.

- An unwrap sits on every datastore read that misses the key cache, so cache behavior and the key service availability target both matter
- Rotation runs continuously rather than as an event, and a stalled rotation has to alarm rather than fall quietly behind
- A revoked workspace needs defined degraded behavior in every service that reads its data, not an unhandled decryption error

## Open Questions

What a revoked key that is later restored means, since that is not the same as never having been revoked: caches, replicas, and search indexes may hold decrypted state and need a stated treatment. The second is how long the key operation log is kept relative to the audit log. It is more sensitive and stays useful for longer, and the retention tiers do not distinguish them.
