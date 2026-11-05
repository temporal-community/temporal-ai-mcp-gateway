---
Name: Self-Serve Dashboard Templates
Owner: Jonas Keller
Status: Approved
Last Updated: 2026-04-07
---

## Context

Every new team builds its first dashboard from scratch and gets it subtly wrong: the wrong date grain, no comparison period, metrics that look similar but are defined differently. The analytics team reviews these after the fact, which is both late and resented.

## Proposal

A small set of templates that encode the conventions, available at creation time.

- Four templates: operational health, funnel, usage, and financial summary
- Metrics resolved through the semantic layer, so definitions are correct by construction
- Comparison period and date grain preset to the convention, changeable but not absent
- A short note in each template explaining what it is for and when it is the wrong choice

## Non-goals

No restriction on building from scratch, and no migration of existing dashboards.

## Risks

Templates propagate whatever they encode, including mistakes, at a speed that hand-built dashboards never achieve. The review burden shifts from many dashboards to four templates, which is a better trade only if the four are actually reviewed with care and revisited.

## Measurement

New dashboards started from a template, review findings per new dashboard, and the share of dashboards resolving metrics through the semantic layer.

## Staffing

The analytics team currently spends its review time spread across every new dashboard. Four templates concentrate that time but do not reduce it: a template needs an owner who revisits it when a metric definition changes in the semantic layer, and that is a standing assignment rather than a project.

## Prior Art

The semantic layer shipped with the same reasoning and the same risk, and its history is the useful precedent. Adoption there came from making the correct path the default path, not from a policy, and the definitions that went stale were the ones nobody owned after the launch quarter. The template note explaining when a template is the wrong choice is borrowed directly from how the semantic layer documents its metrics.

## What Would Change Our Mind

- If new dashboards started from templates but then had every preset changed, the templates encode the wrong conventions rather than teaching them
- If review findings per new dashboard do not fall, the problem was never the starting point
- If teams need a fifth and sixth template within a quarter, four categories is the wrong carving and a more general builder is the better answer

A template that is edited beyond recognition is still a better starting point than a blank dashboard, so partial adoption is not by itself a failure. Presets reverted on most dashboards is.
