---
Name: SCIM Provisioning for Enterprise
Owner: Priya Raman
Status: Draft
Last Updated: 2025-10-07
---

## Background

Enterprise customers provision users by uploading a file or by inviting people one at a time. Deprovisioning is worse: it relies on someone remembering, and our own audits have found accounts active months after the person left the customer's company.

## Proposal

Implement the standard provisioning protocol so identity systems can manage users directly.

- User create, update, and deactivate, with deactivate meaning deactivate and not delete
- Group synchronization mapped to our role model, with the mapping configurable per organization
- A provisioning activity log the customer can read themselves
- Deactivation propagates to session revocation within the standard window

## Scope

The three identity providers that cover most of our enterprise base. Others get the same endpoints and no compatibility promises.

## Risks

Group mapping is where these integrations usually fail, because customer group structures encode history rather than intent. A misconfigured mapping can remove access from everyone in a department at once, so changes to mapping preview their effect before applying.

## Measurement

Accounts deprovisioned within a day of the customer's own offboarding, enterprise onboarding time, and the number of stale active accounts found in the next access audit.

## Rollout

- Create and update first, against one design partner per identity provider
- Deactivate enabled only once that customer has run a full offboarding in a test tenant
- Group synchronization last, with the mapping preview required rather than optional
- Each provider certified separately; passing with one says little about the next

Three design partners is the minimum. The providers differ most in how they express group membership, and an implementation that is correct against one routinely fails against another.

## Interfaces Affected

Deactivate has to reach session revocation, so provisioning writes to the session store and not only to the user record. That is a new caller on a path sign-in currently owns. Deactivation also has to be idempotent under retries, because identity systems resend on any ambiguous response, and a second deactivate that errors reads to the customer as a failed offboarding. The user record gains a provisioning source, so a manual edit to a managed user can be refused rather than silently overwritten.

## Support Impact

The common ticket will be a user who exists in the identity system and not here, or the reverse, and the answer is almost always in the mapping. Support needs the activity log and the current mapping side by side, or every one of these escalates to engineering. The alternative is support reading provider logs they have no access to.
