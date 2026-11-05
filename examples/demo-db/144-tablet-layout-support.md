---
Name: Tablet Layout Support
Owner: Amara Osei
Status: Draft
Last Updated: 2025-08-11
---

## Background

On tablets we render the phone layout scaled up. About seven percent of mobile sessions are on tablets, and their session length is half that of phone sessions despite the device being better suited to our content.

## Proposal

A two-pane layout for tablet sizes, reusing the existing components.

- List and detail side by side above a width threshold, with the threshold set by size class rather than by device
- Keyboard shortcut support, since many tablet users have a keyboard attached
- Drag and drop between panes where the phone version uses a menu
- Orientation handled by reflow rather than by locking

## Scope

The four highest-traffic screens. The remainder keep the scaled layout until the pattern is established.

## Risks

Two-pane layouts double the state a screen must manage, and our navigation model assumes a single stack. Retrofitting it is the real work here and the estimate is weaker than it looks, because nobody has tried it in this codebase.

## Measurement

Tablet session length against the phone baseline, task completion on the four screens, and crash rate on tablets, which is currently slightly elevated and may be related.

## Data We Have

The elevated crash rate is worth resolving before the layout work rather than alongside it. The crashes cluster on orientation change and on one screen that is not among the four, which points at the scaled layout's handling of size changes rather than anything in the new design. If that holds, reflow fixes it as a side effect; if it does not, we will have built a two-pane layout on top of a bug.

- Seven percent of mobile sessions, concentrated in two customer segments
- Session length roughly half the phone figure, with no difference in sessions per week
- Crash rate about a third higher than phone, over a small absolute number

## Sequencing

The navigation stack comes first and ships with no visible change: the existing screens run on a model that can hold two panes while still rendering one. That gives us the retrofit estimate for real rather than on paper, and it is the part most likely to be wrong. The four screens follow one at a time, each behind its own flag.

## Open Questions

Whether a tablet with a keyboard attached should behave like a tablet or like the web application is unresolved, and it decides the shortcut set. A set that half-matches the web is worse than one that either matches it or ignores it. Nobody has settled whether to detect the keyboard or assume one.
