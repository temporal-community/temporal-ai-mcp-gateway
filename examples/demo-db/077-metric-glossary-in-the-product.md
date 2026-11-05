---
Name: Metric Glossary in the Product
Owner: Nikhil Shah
Status: Shipped
Last Updated: 2025-08-04
---

## Background

Metric definitions lived in a wiki page that was correct when written. People reading a dashboard did not go to the wiki, so the definition they used was whatever the metric name suggested, which for several metrics was wrong in a way that mattered.

## Approach

Put the definition where the number is.

- Every metric name in the product links to its definition, sourced from the semantic layer
- The definition shows the owner, the last change date, and the plain-language description
- A glossary view listing all defined metrics, searchable
- Undefined metrics visibly marked as such rather than silently indistinguishable

## Non-goals

No enforcement that every metric be defined. Marking the undefined ones turned out to be sufficient pressure.

## Risks

The risk was definitions drifting from behavior, which would make the glossary actively harmful. Sourcing from the semantic layer rather than from prose means the definition shown is the definition executed, at least for the metrics the layer covers.

## Outcome

Shipped in July. Definition views run about nine hundred a week, and the number of undefined metrics on the main dashboards fell from thirty-one to four within a month of the marking going live, which was faster than any amount of asking had achieved.

## Prior Art

The wiki page was the second attempt. Before it, analytics kept a spreadsheet of definitions that decayed the same way and for the same reason: the definition lived somewhere the reader was not. Two external catalog tools were evaluated at the time. Both indexed warehouse tables rather than the semantic layer, so a definition in the catalog and the expression behind a dashboard number could disagree without anyone noticing, which is the failure this shipped to avoid.

## Operational Impact

Definitions became a release artifact. A change in the semantic layer changes what every reader sees the same day, so a rename made for tidiness now reads as a definition change, and two of those went out before the pattern was recognized. The owner field also routes questions: analytics picked up roughly two hours a week of them that previously went nowhere. That is new work this created, and it is worth stating rather than counting as a win.

## Open Questions

- The four undefined metrics left on the main dashboards have not moved in two months and are all owned by teams that no longer exist in that form
- Whether metrics computed in notebooks, outside the semantic layer, should appear in the glossary at all or stay visibly out of scope
- Whether the last change date should surface prior definitions, since a reader comparing a chart to a screenshot from March needs the March definition
