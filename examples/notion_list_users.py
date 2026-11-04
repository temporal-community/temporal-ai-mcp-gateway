"""Example run_script: list the first few users in the connected Notion workspace.

Run it against a running backend with:
    uv run durable-mcp-gateway call-tool run_script examples/notion_list_users.py

A minimal one-tool example. Upstream tools are async, so wrap the work in an async main and
`await` the call. See notion_find_1pagers_mentioning_ai.py for parallelizing with gather.
"""

import asyncio


async def main():
    users = await notion_notion_get_users(page_size=5)
    names = [u["name"] for u in users["results"]]
    for n in names:
        print(n)
    return names


asyncio.run(main())
