"""Example run_script: search Notion, then fetch the top hit in full.

Run it against a running backend with:
    uv run durable-mcp-gateway call-tool run_script examples/notion_search_and_fetch.py

Upstream tools are async Python functions (see the full typed stub via
`uv run durable-mcp-gateway call-tool list_upstream_tools`). Wrap your work in an async main,
`await` each tool, index results like dicts, and return the value you want back; anything you
print is returned alongside it. A tool failure raises a catchable RuntimeError at its await.
(These two calls are sequential — the fetch depends on the search — so no gather here; see
notion_find_1pagers_mentioning_ai.py for running independent calls concurrently.)
"""

import asyncio


async def main():
    hits = await notion_notion_search(query="meeting notes", page_size=3)
    for r in hits["results"]:
        print("- " + r["title"] + "  (" + r["url"] + ")")

    # Fetch the full contents of the top hit (if any) and return its title as the result.
    if not hits["results"]:
        return "no results"
    top = hits["results"][0]
    doc = await notion_notion_fetch(id=top["id"])
    print("fetched " + repr(doc["title"]) + ": " + str(len(doc["text"])) + " chars")
    return doc["title"]


asyncio.run(main())
