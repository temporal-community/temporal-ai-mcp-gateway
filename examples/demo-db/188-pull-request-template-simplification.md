---
Name: Pull Request Template Simplification
Owner: Ruth Adeyemi
Status: Shipped
Last Updated: 2025-06-20
---

## Background

The change template had eleven sections, accumulated over years as each incident added a checkbox. Most were filled with not applicable, which meant the two sections that mattered were buried in boilerplate that reviewers had learned to scroll past.

## Approach

Cut to three sections and make them count.

- What changed, why, and how it was verified
- Risk-specific checklists moved to a label-triggered comment, appearing only where relevant
- The template measured by whether reviewers read it, not by whether authors fill it
- Removed sections archived with the reasoning, in case a future incident wants them back

## Non-goals

No change to required approvals or to the checks that run.

## Risks

The sections were each added in response to something going wrong, and removing them invites the argument that we are discarding hard-won lessons. The label-triggered checklists kept the lessons available where they apply rather than everywhere.

## Outcome

Shipped in May. Template completion is up from about half to nearly all, and reviewers report in the quarterly survey that the description is now useful, which it previously was not.

## Review Notes

Completion moved partly because the template got shorter and partly because not applicable stopped being an available answer for the three remaining sections. Those two effects cannot be separated from the data we kept, so the number is evidence that the template became fillable, not that authors became more diligent.

## Operational Impact

Label-triggered checklists put a dependency on labels being applied, which nobody had to care about before. Two of the five fire on labels the automation derives from changed paths; three fire on labels a person chooses. The chosen ones are the weak link. A change touching a sensitive area without the label now gets no checklist, where before it got the boilerplate version nobody read. That trades a reliable useless prompt for an unreliable useful one, and it only holds while path-derived labelling keeps expanding.

## What Would Change Our Mind

An incident whose postmortem lands on a removed section would reopen this. The archive exists for that, with the reasoning attached, so the argument would start from what we knew in May rather than from nothing. Adding one section back is cheap. Restoring all eleven because one of them turned out to matter is the move we would refuse.
