---
Name: Experiment Readout Automation
Owner: Amara Osei
Status: Draft
Last Updated: 2025-12-16
---

## Background

Experiment readouts are assembled by hand from a query template. The assembly takes about half a day, which means experiments run longer than needed because the readout is a chore, and it means the statistical treatment varies with who did the work.

## Proposal

Generate the readout from the experiment definition on a schedule.

- Metrics and guardrails declared when the experiment is created, not chosen afterwards
- Daily computation with a fixed statistical method and a stated stopping rule
- Peeking discouraged by design: the decision metric is revealed only at the planned duration
- Readout rendered as a document that can be circulated without reformatting

## Scope

Product experiments on the standard platform. Pricing tests have regulatory and commercial considerations and stay with a human.

## Risks

Automating the readout makes it easy to run more experiments, which is good, and easy to run underpowered ones, which is not. The creation flow should refuse to start an experiment whose declared effect size cannot be detected in the planned duration at the available traffic.

## Measurement

Time from experiment end to circulated readout, experiments stopped early against the stopping rule, and the share of readouts using the standard method.

## Migration

Experiments already running were created without declared metrics, so the generator cannot read them and they should finish on the manual process rather than be retrofitted. The query template becomes the reference implementation of the fixed method and is then retired, since two ways of computing the same readout is how the treatment started varying. Past readouts stay as they were written and are not recomputed.

## Operational Impact

The readout stops being half a day of analyst work and becomes a definition someone has to get right at the start.

- Metric declaration moves the effort to creation time, where it is cheaper and much less negotiable
- The power check will refuse experiments teams expect to run, and that refusal needs an owner who can hold it
- Guardrail breaches need a route that does not wait for the planned duration, since hiding the decision metric must not hide a harm

## Open Questions

Who may override the stopping rule, and what the readout records when they do. An override that leaves no trace makes the rule advisory; one that demands a written reason becomes a document nobody writes. The other is what happens when a declared metric stops being computed mid-experiment because its dataset changed underneath it, where the readout either drops that metric quietly or fails and takes the rest with it.
