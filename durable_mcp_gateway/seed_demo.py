"""``seed-demo``: recreate the demo 1-pager database in your own Notion workspace.

    uv run durable-mcp-gateway seed-demo --parent <page-url>

Creates "Product One-Pagers (Demo)" under the given page, adds one page per file in
``examples/demo-db/`` (front matter for the columns, markdown for the body), and prints the new
data source URL to set as ``DS`` in ``examples/notion_find_1pagers_mentioning_ai.py``.

It calls Notion's MCP tools over its own session, signed in with the token ``connect notion``
stored, rather than through the gateway: a sandboxed script can't read the dump files, and the
gateway isn't meant for write tools.
"""

from __future__ import annotations

import asyncio
import re
import sys
from itertools import batched
from pathlib import Path
from urllib.parse import urlparse

from . import config, upstreams
from .vault import open_default_vault

UPSTREAM = "notion"
DEMO_DB_DIR = Path(__file__).resolve().parent.parent / "examples" / "demo-db"
TITLE = "Product One-Pagers (Demo)"
SCHEMA = (
    'CREATE TABLE ("Name" TITLE, "Owner" RICH_TEXT, '
    "\"Status\" SELECT('Draft':gray, 'In Review':yellow, 'Approved':green, "
    "'Shipped':blue, 'Parked':red), "
    '"Last Updated" DATE)'
)
BATCH_SIZE = 50

_PAGE_ID = re.compile(r"[0-9a-fA-F]{32}$")
_DATA_SOURCE = re.compile(r"collection://[0-9a-fA-F-]{36}")


class _SeedFailed(RuntimeError):
    pass


def _page_id(parent: str) -> str:
    match = _PAGE_ID.search(urlparse(parent).path.rstrip("/").replace("-", ""))
    if match is None:
        raise SystemExit(f"--parent: no Notion page ID in {parent!r}")
    return match.group(0)


def _load_pages(directory: Path) -> list[dict]:
    pages = []
    for path in sorted(directory.glob("*.md")):
        _, front, body = path.read_text().split("---\n", 2)
        fields = dict(line.split(": ", 1) for line in front.splitlines())
        pages.append(
            {
                "properties": {
                    "Name": fields["Name"],
                    "Owner": fields["Owner"],
                    "Status": fields["Status"],
                    "date:Last Updated:start": fields["Last Updated"],
                    "date:Last Updated:is_datetime": 0,
                },
                "content": body.strip("\n"),
            }
        )
    return pages


async def _call(session, tool: str, arguments: dict) -> str:
    result = await session.call_tool(tool, arguments)
    text = upstreams.join_text_blocks(result.content)
    if upstreams.is_error(result):
        raise _SeedFailed(f"{tool} failed: {text}")
    return text


async def _seed(server_cfg: dict, page_id: str, pages: list[dict]) -> str:
    token_storage = None
    if upstreams.is_oauth(server_cfg):
        token_storage = open_default_vault().storage_for(config.LOCAL_USER_ID, UPSTREAM)
    async with upstreams.upstream_session(server_cfg, token_storage) as session:
        created = await _call(
            session,
            "notion-create-database",
            {"parent": {"page_id": page_id}, "title": TITLE, "schema": SCHEMA},
        )
        match = _DATA_SOURCE.search(created)
        if match is None:
            raise _SeedFailed(f"notion-create-database returned no data source URL:\n{created}")
        data_source = match.group(0)
        print(f"Created {TITLE!r}: {data_source}", file=sys.stderr, flush=True)
        done = 0
        for batch in batched(pages, BATCH_SIZE):
            await _call(
                session,
                "notion-create-pages",
                {
                    "parent": {"data_source_id": data_source.removeprefix("collection://")},
                    "pages": list(batch),
                },
            )
            done += len(batch)
            print(f"  {done}/{len(pages)} pages", file=sys.stderr, flush=True)
    return data_source


def seed_demo(parent: str) -> None:
    """Create the demo database under ``parent`` (a Notion page URL or ID) and print its data
    source URL."""
    page_id = _page_id(parent)
    servers = {s["name"]: s for s in upstreams.load_servers()}
    server_cfg = servers.get(UPSTREAM)
    if server_cfg is None:
        raise SystemExit(
            f"no {UPSTREAM!r} upstream in {upstreams.UPSTREAMS_PATH}; add it (see "
            f"examples/upstreams.json), then run: {config.CONNECT_HINT} {UPSTREAM}"
        )
    pages = _load_pages(DEMO_DB_DIR)
    if not pages:
        raise SystemExit(f"no demo pages in {DEMO_DB_DIR}; run seed-demo from a repo checkout")

    try:
        data_source = asyncio.run(_seed(server_cfg, page_id, pages))
    except* upstreams.ReconnectRequired:
        raise SystemExit(
            f"upstream {UPSTREAM!r} is not authorized; run: {config.CONNECT_HINT} {UPSTREAM}"
        )
    except* _SeedFailed as group:
        raise SystemExit(str(group.exceptions[0]))

    print(
        f"Seeded {len(pages)} pages. Set DS in "
        f"examples/notion_find_1pagers_mentioning_ai.py to:\n{data_source}"
    )
