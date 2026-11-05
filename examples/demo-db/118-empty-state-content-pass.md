---
Name: Empty State Content Pass
Owner: Omar Haddad
Status: Draft
Last Updated: 2025-08-29
---

## Problem

Empty states across the product say some variation of nothing here yet. They do not say what would be here, how to put something here, or whether empty is a problem. For a new workspace, nearly every screen is an empty state, so this is most of the first-run experience.

## Proposal

Rewrite every empty state to do three things: name what belongs here, offer the action that creates it, and show an example where one helps.

- An inventory of all empty states, which nobody currently has
- A consistent structure: what, why, and one action
- Illustrative examples where the concept is unfamiliar, suppressed where it is obvious
- Empty states that are the result of a filter distinguished from those that mean genuinely nothing exists

## Scope

The web product. Mobile has fewer empty states and should follow the same patterns once settled.

## Risks

The filter case is the one that matters most and is most often missed: telling someone to create their first item when they have four hundred and a filter applied is actively insulting. Distinguishing the two requires the component to know which it is, which several of ours currently do not.

## Measurement

Empty states rewritten, action-taken rate from empty states, and first-week activation for new workspaces.

## Sequencing

The inventory goes first and is the item most likely to be skipped, because it produces nothing anyone can see. Without it the rewrite covers the screens somebody remembered and misses the ones reached only through a filter or a deep link, which are disproportionately the ones that look broken. The filter-versus-genuinely-empty distinction comes next; it is component work and it gates the copy for roughly a third of the inventory. Copy comes last, written by surface rather than by screen, so states that sit beside each other read as though one person wrote them.

## Dependencies

- Components that can tell a filtered result from an empty collection, which several cannot today, making this engineering work that precedes any writing
- Illustration capacity for the example states, the slowest input here, which should be spent only on concepts that are genuinely unfamiliar
- A home for the pattern itself, or the next feature built ships a nothing-here-yet of its own and the inventory starts growing again

## Review Notes

- One action per empty state is the rule worth holding; a state offering three actions is one whose author could not decide what belongs there
- The example should be dismissible by the person looking at it, since it stops helping on the second visit and starts occupying the screen
- A failed load is a third case this proposal does not name, and treating it as empty is how a broken screen comes to read as an invitation
