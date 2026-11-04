"""Find recent 1-pagers in the Product Proposal database whose BODY mentions AI or agents.

    uv run durable-mcp-gateway call-tool run_script examples/notion_find_1pagers_mentioning_ai.py

Why this is a good fit for the gateway: the filter is on each page's *body*, not its title or
properties. Done against the Notion MCP directly, an agent would have to read every 1-pager's
full body into its context to check it — a huge token bill. Here it's one enumeration query
plus a server-side loop; only the short list of matching links comes back to the model.

Upstream tools are async: we `await asyncio.gather(...)` the page fetches so they run
CONCURRENTLY (as parallel Temporal activities) instead of one-at-a-time. Transient upstream
errors (Notion loves to 429) are retried durably by the gateway, so gather doesn't need
per-item error handling here.

Sandbox notes: no imports except asyncio; the text match uses plain string ops. "agent" is a
substring match (catches agent/agents/agentic); "AI" is matched at word level (so it does NOT
fire on 'email', 'detail', 'available', 'maintain', ...).
"""

import asyncio

DS = "collection://1f38fc56-7738-80b5-afad-000bbfbe4193"
# Cap the scan so the demo runs quickly. Bump it to scan more; the DB is 140+ 1-pagers.
LIMIT = 100


def mentions_ai_or_agent(text: str) -> bool:
    body = text.lower()
    if "agent" in body:
        return True
    # Word-level "ai": normalize punctuation to spaces, then look for the standalone token.
    for ch in ".,;:!?()[]{}\"'`/\\|<>=+*&^%$#@~-\n\t\r":
        body = body.replace(ch, " ")
    return "ai" in body.split()


async def main():
    # 1. Enumerate the LIMIT most-recently-created rows (Name, url) — one query.
    #    createdTime is the canonical creation timestamp; DESC gives newest first.
    page = await notion_notion_query_data_sources(
        data={
            "data_source_urls": [DS],
            "query": 'SELECT "Name", url FROM "'
            + DS
            + '" ORDER BY createdTime DESC LIMIT '
            + str(LIMIT),
        }
    )
    rows = page["results"]
    print("scanning the " + str(len(rows)) + " most recent 1-pagers")

    # 2. Fetch every page body concurrently, then keep the ones mentioning AI or agents.
    #    gather() requests them all at once; the worker's max_concurrent_activities caps how
    #    many actually run in parallel (the rest queue), so this stays polite to the upstream.
    docs = await asyncio.gather(*[notion_notion_fetch(id=r["url"]) for r in rows])
    matches = []
    for i in range(len(rows)):
        if mentions_ai_or_agent(docs[i].get("text") or ""):
            matches.append({"name": rows[i]["Name"], "url": rows[i]["url"]})

    print("matched " + str(len(matches)) + " of " + str(len(rows)))
    for m in matches:
        print("- " + str(m["name"]) + ": " + m["url"])
    # The result is just the matching links — a few KB, vs. the megabytes of page bodies the
    # model would otherwise have had to read.
    return matches


asyncio.run(main())
