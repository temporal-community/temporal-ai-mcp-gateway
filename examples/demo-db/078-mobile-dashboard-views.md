---
Name: Mobile Dashboard Views
Owner: Clara Benton
Status: Parked
Last Updated: 2025-10-02
---

## Problem

Dashboards are opened on phones more than we expected, mostly by leadership checking a number between meetings. The layout does not adapt, so the experience is pinch-and-scroll over a chart grid designed for a wide screen.

## Proposal

A mobile presentation mode that reflows rather than scales.

- A single column of cards ordered by the dashboard's own layout order
- Charts simplified at small sizes: fewer series, no legend, larger touch targets
- A summary number at the top of each card, visible without interaction
- Filters collapsed into a sheet rather than occupying the viewport

## Scope

Viewing only. Editing on a phone is a different product and not one anyone has asked for.

## Risks

Simplifying a chart changes what it says, and a chart with series removed can imply a trend the full version contradicts. Deciding what to drop is a judgment per chart type, not a generic rule, which is more design work than this is currently funded for. Parked for that reason rather than for lack of demand.

## Measurement

If it proceeds: mobile dashboard sessions, time to first meaningful view, and whether leadership stops asking people to send them screenshots.

## Data We Have

Phone sessions are about fourteen percent of dashboard views and concentrate on six dashboards, all of them summaries rather than working analyses. The median session on a phone is under forty seconds. That shape suggests the problem is narrower than a general mobile mode: these people want one number, and reflowing a twenty-chart operational dashboard may never be worth the design it would take.

## Alternatives Considered

- A mobile layout authored per dashboard by whoever owns it, which gives correct results and asks for work from people who will not do it
- Sending the summary numbers as a scheduled message instead of a view, which serves the between-meetings case and nothing else
- Rendering the existing layout to a phone-sized image, which is what people already do by hand with screenshots and is at least honest about not adapting

## Staffing

The constraint is design time, not engineering. A rule set covering what to drop in each of the nine supported chart types is four to six weeks of design work, and none of it is allocated. The engineering behind it is smaller and cannot sensibly go first: building the reflow before the rules exist means the rules get chosen by whoever writes the layout code, which is the outcome the risks section is trying to avoid.
