"""Input/output models that cross the Workflow/Activity boundary.

No ``from __future__ import annotations`` here — these models cross Temporal's pydantic
converter, and stringized annotations leave its TypeAdapter machinery "not fully defined".
Keep annotations concrete.
"""

from typing import Any

from pydantic import BaseModel


class RunScript(BaseModel):
    r"""Run a Python ``script`` to completion in the pydantic-monty sandbox.

    **Do the whole task in one script.** When a task spans many tool calls — especially
    fanning out over a list (fetch N items, check each, collect the matches) — write ONE
    script that does the entire thing: enumerate, loop/gather the calls, and filter/aggregate
    inside the script, returning only the final answer. Do NOT run one script per item, and do
    NOT return raw intermediate data (whole page bodies, full listings) just to inspect it —
    that pulls everything back into your context, bloats your memory, and costs the user lots of money. Keep the big data in
    the sandbox; return only the small result.

    The script is **not** plain CPython — it runs in `pydantic-monty
    <https://pypi.org/project/pydantic-monty/>`_, a sandboxed interpreter with no network,
    filesystem, or ambient I/O (only ``import asyncio`` is available, for concurrency).
    Ordinary in-sandbox Python works (arithmetic, comprehensions, f-strings, ``print`` —
    captured and returned to you).

    Upstream MCP tools are exposed as **async** functions — one per tool, called by keyword
    arguments. You must ``await`` them, and should ``asyncio.gather(...)`` independent calls to
    run them **concurrently**. NOTE: the sandbox's asyncio is minimal — ``gather(*coros)`` takes
    ONLY positional coroutines, no keyword args (so **no** ``return_exceptions=True``), and there
    is no ``Semaphore`` or ``async with``; gather every call and let a failure raise. Call the
    ``list_upstream_tools`` tool to get the typed stub
    naming every function and its arguments/result; the script is statically **type-checked**
    against that stub before it runs, so unknown functions, missing/extra arguments, wrong
    types, and a missing ``await`` are reported up front. A tool returns the typed result the
    stub shows, usually a dict you index with ``result["key"]``. When a tool declares no output
    schema that type is **learned** from what past calls returned, so it is incomplete: indexing
    a field it does not list is a type error, and ``result.get("field")`` is the way to reach
    one it has not seen. A learned type does not guarantee the result is a dict on any given
    call, so check before indexing. A tool with no schema and nothing learned yet returns whatever the
    upstream sent — a dict, a list, a string, a number, or ``None`` for a plain-text result —
    so check it before indexing. A tool **failure**
    raises a catchable ``RuntimeError`` at its await.

    The value of the script's **last expression** becomes the result (alongside anything
    it printed). So end your script with the value you want back.

    EXAMPLE — the RIGHT shape for "which of these pages mention X in the body?": one script,
    bodies filtered in the sandbox, only the links come back:
        import asyncio
        async def main():
            rows = (await notion_notion_query_data_sources(data={...}))["results"]
            docs = await asyncio.gather(*[notion_notion_fetch(id=r["url"]) for r in rows])
            return [r["url"] for r, d in zip(rows, docs) if "x" in d["text"].lower()]
        asyncio.run(main())
    """

    script: str
    # Opaque vault handle the stdio server injects (NOT supplied by the model). Resolves
    # to a user so upstream tool calls use that user's OAuth tokens. Empty when the
    # caller has no session (e.g. the debug harness) — fine for non-OAuth upstreams.
    session_id: str = ""


class CallToolRequest(BaseModel):
    """Internal name+arguments model for a tool call crossing the Workflow/Activity boundary."""

    name: str
    arguments: dict
    # Threaded from RunScript so the Activity can resolve the user and pick the
    # right OAuth token from the vault for an OAuth-protected upstream.
    session_id: str = ""


class CallToolResult(BaseModel):
    """Internal result envelope of a tool call (Activity → Workflow); the Workflow unwraps it.

    On failure ``result`` is None."""

    ok: bool
    result: Any = None
    error: str | None = None


class Catalog(BaseModel):
    """The discovered tool catalog the stdio server serves: the typed Python ``stub`` and the
    raw JSON ``tools`` list."""

    stub: str
    tools: list[dict]
