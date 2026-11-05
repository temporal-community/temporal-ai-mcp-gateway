---
Name: Attribution Model Refresh
Owner: Dana Whitfield
Status: Draft
Last Updated: 2025-09-30
---

## Context

Acquisition is attributed last-touch, which assigns nearly everything to branded search and tells us to spend more on the channel people use after they have already decided. The marketing team does not believe the numbers, which means they make decisions on something else.

## Proposal

Move to a position-based model with a documented decay, and publish both during a transition.

- Touchpoints collected across a ninety-day window with consistent identity resolution
- A position-based model with weights agreed with marketing rather than chosen by us
- Both models reported side by side for two quarters
- The model definition versioned and the change log visible on every report

## Non-goals

No attempt at incrementality measurement. That requires holdouts and a different kind of investment, and it is the right next step rather than this step.

## Risks

Any multi-touch model is a set of assumptions dressed as a measurement, and the weights will be argued about forever. Agreeing them with marketing in advance, in writing, is the only thing that makes the output usable. Running both for two quarters is what lets channel budgets move gradually rather than lurching.

## Measurement

Channel mix under each model, marketing's stated confidence in the numbers, and whether budget decisions begin citing the new model.

## Data We Have

Touchpoint collection is the weak link here, not the model.

- Paid click data is complete for two years and carries a campaign identifier on every row
- Organic and direct visits use a session identity that breaks across devices, which is where the ninety-day window loses people
- Offline touches, including events and outbound conversations, sit in another system and are not joined today

Identity resolution decides how much of that window is real. If a third of journeys fragment, a position-based model mostly moves weight around inside the fragment it can see, and the first touch it credits is not the first touch.

## Timeline

Identity resolution and touchpoint collection come first and take a quarter. The weights can be agreed in parallel, since that is a conversation rather than a build. The two-quarter side-by-side period starts when a first complete month exists under both models, not when the pipeline first runs, because that month is where the collection gaps surface. Incrementality stays out until the side-by-side reporting has finished.

## Open Questions

What happens when the weights are reopened, which the risks section all but promises. Versioning the definition makes a change visible; it does not say who approves one, or whether a change applies to history as well as to new reporting. Restating a past quarter under new weights is defensible and turns every report into a moving target, and the transition is exactly when someone will ask for it.
