---
Name: Category Taxonomy Refresh
Owner: Amara Osei
Status: Draft
Last Updated: 2025-09-11
---

## Background

The category tree has three hundred nodes, added one at a time as sellers asked. Several categories overlap, the deepest branch is seven levels, and about a fifth of listings sit in a catch-all at the top level because nothing fits.

## Proposal

Restructure from how buyers search rather than from how the tree grew.

- A new tree derived from search query clustering and from buyer card sorting
- Maximum depth of four, with attributes carrying the detail that depth currently carries
- Listings migrated automatically where the mapping is unambiguous, with sellers prompted where it is not
- Old category paths redirected rather than broken, since they are linked externally

## Scope

The category tree and listing migration. Attribute schema per category is a dependent piece of work.

## Risks

Recategorization moves listings away from the places sellers have optimized for and buyers have bookmarked, and the short-term effect on traffic distribution will be significant and uneven. Sellers whose traffic falls will attribute it to this change whether or not it caused it.

## Measurement

Listings in the catch-all category, search queries resolving to a category, tree depth distribution, and traffic variance per seller through the migration.

## Dependencies

Attributes are the load-bearing dependency. Cutting depth from seven to four works only if the detail that lived in the deep nodes has somewhere to go, and that somewhere is the attribute schema, which runs on its own timeline. Migrating a branch before its attributes exist flattens real distinctions into nothing. Search ranking also reads the tree, so the ranking team needs the new structure in a test index before the migration rather than after it.

## Sequencing

Branches migrate independently, so the order is a choice, and the first should be the branch where the catch-all problem is worst rather than the one that is easiest. Redirects go in with the first branch and stay for at least a year, since external links are the part we do not control. Seller prompts for ambiguous listings arrive per branch, so a seller with listings across four branches is not handed one request covering everything they own.

## Support Impact

Sellers will attribute traffic changes to the migration, and most of those contacts are unanswerable without per-seller numbers.

- Traffic variance per seller is published to that seller with the pre-migration baseline beside it
- A route to dispute an automatic mapping, which is cheaper than a wrong category staying wrong
- The catch-all is not retired on the first pass, since listings that fit nowhere still need somewhere to sit
