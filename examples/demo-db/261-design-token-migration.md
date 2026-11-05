---
Name: Design Token Migration
Owner: Erin Vasquez
Status: Draft
Last Updated: 2025-10-04
---

## Context

Color, spacing, and type values are hard-coded across the product in hundreds of places. There are nineteen distinct greys. A theme change, which is now required for the accessibility work, would mean touching every one of them by hand.

## Proposal

Extract values into tokens and migrate surfaces incrementally.

- A token set covering color, spacing, type scale, and radius, defined once
- Semantic naming by role rather than by value, so a token can change without becoming a lie
- Automated migration where the mapping is unambiguous, which is most of the spacing and type
- Color migrated by hand, since the nineteen greys do not map cleanly to a smaller set

## Scope

The web product. The mobile applications have their own system and should adopt the same token values through a shared definition.

## Risks

Semantic naming requires deciding what each value means, and for the ambiguous cases the decision will be wrong somewhere, producing a token used in a place it was not meant for. That is recoverable; naming tokens after their values, which is tempting and fast, is not.

## Measurement

Hard-coded values remaining, distinct color values in use, and the effort required to apply a theme change, which is the thing this exists to enable.

## Sequencing

Spacing and type go first because they are automatable, and because finishing them demonstrates the token set before the arguments about color start. Color follows surface by surface, with the nineteen greys resolved into a decided set beforehand rather than during the substitution.

- Token set defined and published, including the shared definition the mobile applications consume
- Spacing, type scale, and radius migrated automatically, one repository-wide change per category
- Grey resolution settled as a design question, documented with which old value maps where
- Color migrated by surface, starting with the surfaces the accessibility work touches first

## Staffing

The automated part is a week. Hand-migrated color is the schedule: nineteen greys across the surfaces using them is one design decision followed by a few hundred small edits. Splitting those across the teams that own the surfaces is faster than one person doing all of it and produces inconsistent judgment calls, so one owner decides the mapping and teams apply it.

## Interfaces Affected

- The component library, which has to consume tokens before any product surface can
- The mobile shared definition, which needs a format both platforms can build from
- The accessibility theme work, the first consumer and the reason the semantic names have to be right
- Design tooling, where token names have to match what engineers see, or the handoff reintroduces raw values
