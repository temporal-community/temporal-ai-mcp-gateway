---
Name: AI Vendor Access Review
Owner: Jonas Keller
Status: In Review
Last Updated: 2026-05-14
---

## Context

We now have eleven third-party vendors with some form of access to internal systems, up from four two years ago. Access was granted at purchase time under whatever terms the contract specified, and nobody has looked at the set as a whole since.

## Proposal

A standing quarterly review of vendor access, with a single inventory behind it.

- One inventory row per vendor: the systems reached, the data categories touched, the credential type, and the internal owner
- Credentials issued to vendors tagged as such, so they can be enumerated rather than inferred
- A quarterly review where each owner confirms the access is still needed at the scope granted
- Automatic flagging of vendor credentials unused for sixty days

## Scope

Vendors with direct system access. Processors that only receive data through an export are covered by a different control and are not in this inventory.

## Risks

The inventory is only as good as its maintenance, and quarterly reviews decay into a signature exercise within a year unless something forces attention. The unused-credential flag is that forcing function, because it produces a specific question about a specific credential rather than asking an owner to review a list.

## Measurement

Vendors in the inventory versus vendors in procurement records, which should converge, and the number of credentials revoked per review cycle.

## Data We Have

Procurement holds contracts for fourteen vendors whose terms mention system access; the platform team knows of eleven. Reconciling those two lists is the first week of work, and the gap is probably two renewals and a pilot that was never ended. Credential tagging does not exist yet, so today's count of vendor credentials is assembled from naming conventions and two people's recollection. Last-use timestamps are available through the identity provider but not for the four vendors holding long-lived keys on the data platform, which is exactly where the sixty-day flag would matter most and where it will not work in the first cycle.

## Alternatives Considered

- Review at contract renewal, which matches how access was granted but can leave eleven months between an engagement ending and anyone noticing
- Expiring every vendor credential at ninety days, rejected because the renewal work lands on the internal owner whether or not anything changed
- Folding this into the employee access review, which uses a different ownership record and would bury eleven rows among several thousand

## Operational Impact

Each internal owner picks up one confirmation per quarter, which is small, plus whatever the unused-credential flags raise, which is not predictable in the first two cycles. Revocation needs a path that does not depend on the vendor cooperating, since the case that matters is the one where the relationship has already ended badly. A credential that is flagged and still needed has to record why, or the same flag comes back next quarter to the same shrug.
