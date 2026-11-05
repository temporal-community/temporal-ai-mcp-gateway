---
Name: Column-Level Lineage
Owner: Dmitri Volkov
Status: Draft
Last Updated: 2025-10-23
---

## Background

Lineage today is table to table, which answers the question nobody asks. The real question, when a number looks wrong, is which upstream column it came from and what transformed it, and answering that means reading the transformation code by hand.

## Proposal

Parse the transformation definitions to produce column-level lineage, refreshed on every deployment.

- Parsed from the query definitions rather than inferred from runtime observation
- Rendered as a graph with the ability to walk upstream from any column
- Annotated with the last successful load time for each node
- Exposed in the catalog alongside the column description

## Scope

Transformations expressed in the modeling framework, which is about eighty percent of the warehouse. Hand-written loading jobs remain table-level until they are migrated.

## Risks

Parsed lineage is confidently wrong in the presence of dynamic query construction, and we have perhaps forty models that build their queries from configuration. Those need to be flagged as unparsed rather than quietly given incomplete lineage, which would be worse than none.

## Measurement

Columns with resolved lineage as a share of the total, time to trace a suspect number to its source, and use of the lineage view during incidents.

## Cost

The parse runs on every deployment and the graph it produces is rebuilt whole rather than patched. At the current model count that is minutes, not hours, and it runs after the deployment rather than gating it. Storage is negligible next to the warehouse itself.

The real cost is maintenance of the parser against the modeling framework's own changes. Every framework upgrade can change how a definition resolves, and a parser that silently falls behind produces lineage that looks current and is not.

## Failure Modes

- A parse failure on one model should mark that model unparsed, not abort the graph build
- A model whose lineage resolves but resolves wrongly is the dangerous case, and dynamic query construction is where it happens
- The last successful load annotation goes stale if the graph is rebuilt from definitions while load times come from a separate source
- A deployment that renames a column leaves the old node in the catalog until the next full rebuild

## Dependencies

The catalog has to accept a lineage attachment per column, which it does not today. Load times come from the orchestrator's run history, so the graph build has to read it rather than infer freshness from the warehouse. Neither is large, but both are owned elsewhere and both have to land before the view is useful enough to use during an incident.
