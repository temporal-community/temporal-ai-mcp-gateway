---
Name: Icon Set Consolidation
Owner: Victor Alves
Status: Shipped
Last Updated: 2025-06-13
---

## Background

The product used icons from three sources plus a folder of one-off drawings. Two visually different icons were used for the same action in different places, and several icons were used for different actions in different places, which is the worse failure.

## Approach

One set, mapped by meaning rather than by appearance.

- An audit of every icon in use and the action it represented
- A single set chosen for coverage, with gaps commissioned rather than improvised
- A meaning-to-icon mapping documented, so the same action always gets the same icon
- One-off drawings removed, with their meanings mapped into the set

## Non-goals

No change to layout or to which actions are iconized rather than labeled.

## Risks

The audit was the work. Mapping by appearance would have been fast and would have preserved the existing inconsistencies in a tidier form, which is how icon consolidation usually fails.

## Outcome

Shipped in May. Icon count fell from about four hundred to one hundred and seventy, the duplicated-meaning cases are gone, and the shipped bundle is meaningfully smaller, which was an unplanned benefit.

## Migration

The replacement went out screen by screen over six weeks rather than as one swap. A simultaneous change would have landed every visual regression at once with no way to tell which mapping decision caused which complaint. Screens were ordered by traffic, lowest first, so the mapping had three weeks of correction before reaching the screens most people see.

- Old icon references stayed resolvable through the migration, pointing at their mapped replacement
- The one-off drawings folder was deleted only after the last reference moved
- Each screen's change was reviewed against the mapping, not against a screenshot

## Operational Impact

The mapping document is now the thing that has to be maintained. Adding an action to the product means choosing a meaning before choosing an icon, which is a small extra step and the entire mechanism. A lint rule rejects an icon reference that is not in the mapping, and that is what keeps a fourth source from appearing.

## Open Questions

What happens when the chosen set redraws an icon upstream is undecided. A redraw changes appearance without changing meaning, which the mapping tolerates and customers may not. Taking upstream updates automatically is cheap and occasionally surprising; pinning the version is safe and gradually leaves us on an old set.
