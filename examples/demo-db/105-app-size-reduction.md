---
Name: App Size Reduction
Owner: Jonas Keller
Status: Draft
Last Updated: 2025-10-09
---

## Background

The application binary is now large enough that a meaningful share of installs on cellular connections do not complete. Our install funnel shows a drop between store tap and first open that correlates with connection type and with the size increases of the last three releases.

## Proposal

Attack the three largest contributors and establish a budget so this does not recur.

- The bundled font set reduced to what the supported locales require, with the rest fetched
- Image assets converted to a modern format and stripped of unused variants
- The analytics library replaced with a thin client, which accounts for a surprising share
- A size budget enforced in the build, failing the pipeline on regression

## Scope

Both platforms, with the budget per platform since their baselines differ.

## Risks

Fetching fonts on demand moves a size cost into a latency cost at first use, which for a text-heavy application is visible. The fetch needs to happen during onboarding rather than at first render, and the fallback has to be acceptable rather than obviously broken.

## Measurement

Download size per platform, install completion rate by connection type, and first-render time, watched as the guardrail.

## Sequencing

The thin analytics client goes first. It is the only one of the three with no user-visible behavior attached, so it ships alone and its size drop is readable against the install funnel with nothing else moving. Images follow for the same reason. Fonts go last, because that is the change trading size for latency and it needs the onboarding fetch built first.

- Thin analytics client alone, funnel watched for two releases
- Image conversion and unused variant stripping
- Font set reduction, after the onboarding fetch and fallback exist
- Budget enabled once all three have landed against the new baseline

## Dependencies

The modern image format is unsupported on the oldest operating system versions still inside the support window, so either those builds carry both asset sets or the window moves. Carrying both is the smaller decision and gives back most of the saving on exactly the devices with the weakest connections, which is worth saying plainly before it is chosen by default.

## Failure Modes

A per-platform budget will eventually be breached by a release with nothing to do with assets, usually a dependency upgrade, and the pressure then is to raise the budget rather than examine the upgrade. The failure should carry a per-component breakdown, so the conversation starts from what grew instead of from the total.
