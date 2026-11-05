---
Name: Interview Scheduling Load
Owner: Dmitri Volkov
Status: Draft
Last Updated: 2025-11-17
---

## Context

Scheduling an interview panel takes a recruiter between thirty minutes and two days of back-and-forth. Candidates wait, panels get rearranged, and the coordination work scales directly with hiring volume, which is growing.

## Proposal

Automated scheduling against interviewer availability with explicit load limits.

- Interviewer availability from their own calendars, with a declared weekly interview budget
- Automatic panel assembly respecting required skills, budgets, and recent load
- Candidate-facing slot selection rather than a proposal exchange
- Rescheduling handled by the same mechanism rather than manually

## Scope

Engineering interviews, which are the highest volume and most structured.

## Risks

Automated assembly will repeatedly select the most available interviewers, who are not necessarily the best ones, and a weekly budget caps that without fixing it. Distribution should be monitored explicitly rather than assumed to follow from the budget.

## Measurement

Time from request to scheduled panel, recruiter hours per hire, interviewer load distribution, and candidate reschedules.

## Dependencies

Reading interviewer calendars needs access the recruiting tool does not hold today, and the grant has to be narrow: free-and-busy only, since panel assembly needs to know when someone is unavailable and nothing about why. The skills each round requires also have to be recorded somewhere a program can read. They currently live in the hiring manager's head and in job description prose.

- Free-and-busy calendar access for interviewers who opt in
- Required skills recorded per round on the interview plan rather than in prose
- Weekly budgets declared by interviewers and visible to their manager

## Rollout

One job family for a quarter, with recruiters able to override any assembled panel and the reason recorded. Those reasons are the design input for the second family: an override saying wrong seniority means the skill model is too coarse, while one naming a specific person means the load distribution is being worked around rather than fixed. Launching without overrides would schedule faster and teach nothing about why it was wrong.

## Open Questions

Whether candidate slot selection shows a wide window or a narrow one is unsettled. A wide window is accepted sooner and spreads panels across weeks, which pushes out time to offer. A narrow one does the reverse and raises reschedules. Nothing in the current data says which costs more.
