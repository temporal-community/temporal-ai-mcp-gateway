"""The MCP server the gateway exposes downstream.
"""

from __future__ import annotations

import asyncio
import json
from datetime import timedelta
from typing import Awaitable, Callable
from uuid import uuid4

import mcp.types as types
from mcp.server.lowlevel import Server
from temporalio.client import Client, WorkflowExecutionStatus, WorkflowFailureError
from temporalio.exceptions import TimeoutError as TemporalTimeoutError

from durable_mcp_gateway import config, vault as vault_mod
from durable_mcp_gateway.models import Catalog, RunScript
from durable_mcp_gateway.workflow import GetCatalogWorkflow, RunScriptWorkflow


class BackendUnavailable(RuntimeError):
    """Raised by the client provider when the durable backend can't be reached."""


async def fetch_catalog(
    get_client: Callable[[], Awaitable[Client]], task_queue: str
) -> Catalog:
    """Fetch the live catalog from the backend's registry over Temporal.

    Bounded by an execution timeout so a server-up-but-worker-down backend degrades to
    :class:`BackendUnavailable` instead of hanging forever waiting for a poller.
    """
    client = await get_client()
    try:
        return await client.execute_workflow(
            GetCatalogWorkflow.run,
            id=f"get-catalog-{uuid4()}",
            task_queue=task_queue,
            execution_timeout=timedelta(seconds=10),
        )
    except WorkflowFailureError as e:
        if isinstance(e.cause, TemporalTimeoutError):
            raise BackendUnavailable(str(e)) from e
        raise


async def list_upstream_tools_text(
    get_client: Callable[[], Awaitable[Client]], task_queue: str
) -> str:
    """The exact text the ``list_upstream_tools`` MCP tool returns: the typed stub, or a
    commented "backend not reachable" note. Shared by the tool handler and the CLI so both
    emit byte-identical output."""
    try:
        catalog = await fetch_catalog(get_client, task_queue)
    except BackendUnavailable as e:
        return (
            f"# Durable backend not reachable at {config.TEMPORAL_ADDRESS} "
            f"({e}); start it with: {config.BACKEND_DOWN_HINT}\n"
        )
    return catalog.stub


async def list_upstream_tools_as_json_text(
    get_client: Callable[[], Awaitable[Client]], task_queue: str
) -> str:
    """The exact text the ``list_upstream_tools_as_json`` MCP tool returns. Shared by the
    tool handler and the CLI."""
    try:
        catalog = await fetch_catalog(get_client, task_queue)
    except BackendUnavailable as e:
        payload = {
            "tools": [],
            "note": (
                f"Durable backend not reachable at {config.TEMPORAL_ADDRESS} "
                f"({e}); start it with: {config.BACKEND_DOWN_HINT}."
            ),
        }
    else:
        payload = {"tools": catalog.tools}
    return json.dumps(payload)


def _backend_down_text(e: Exception) -> str:
    return (
        f"Durable backend not reachable at {config.TEMPORAL_ADDRESS} "
        f"({e}). Start it in a terminal with:\n    {config.BACKEND_DOWN_HINT}"
    )


def _timeline_url(workflow_id: str, run_id: str | None) -> str:
    """The live Temporal Web UI timeline for a workflow run."""
    run = run_id or ""
    return (
        f"http://localhost:{config.TEMPORAL_UI_PORT}/namespaces/"
        f"{config.TEMPORAL_NAMESPACE}/workflows/{workflow_id}/{run}/timeline"
    )


async def run_script_text(
    get_client: Callable[[], Awaitable[Client]],
    task_queue: str,
    script: str | None,
    session_provider: Callable[[], Awaitable[str]],
    wait_seconds: float | None = None,
) -> str:
    """The exact text the ``run_script`` MCP tool returns for ``script``. Shared by the tool
    handler and the CLI.

    Starts the durable Workflow, then waits up to ``wait_seconds`` for it to finish: if it
    completes in time, returns the reply; otherwise returns a handle + a live Temporal UI link
    and tells the agent to point the user at it (the script keeps running; follow it with
    ``wait_script_result`` / ``check_script_result``). ``wait_seconds=None`` blocks for the
    full result (used by the debug CLI, which has no follow-up tools).

    ``session_provider`` mints/returns the opaque session id threaded into the Workflow (so
    ``call_tool_activity`` can resolve the right OAuth token); it's called only after the
    backend is confirmed reachable, so a bad-script or backend-down reply costs no session.
    """
    if not isinstance(script, str) or not script.strip():
        return "run_script requires a non-empty 'script' string."
    try:
        client = await get_client()
    except BackendUnavailable as e:
        return _backend_down_text(e)
    session_id = await session_provider()
    handle = await client.start_workflow(
        RunScriptWorkflow.run,
        RunScript(script=script, session_id=session_id),
        id=f"run-script-{uuid4()}",
        task_queue=task_queue,
    )
    if wait_seconds is None:
        return await handle.result()
    try:
        # On timeout this cancels the local result poll only — the workflow keeps running on
        # the server; we hand back a handle to follow it.
        return await asyncio.wait_for(handle.result(), timeout=wait_seconds)
    except asyncio.TimeoutError:
        url = _timeline_url(handle.id, handle.first_execution_run_id)
        return (
            f"Script still running after {wait_seconds:.0f}s (normal for a long fan-out); it "
            f"keeps running on the backend.\n"
            f"handle: {handle.id}\n"
            f"live progress: {url}\n"
            f"TELL THE USER they can watch execution progress at that URL. Then call "
            f"`wait_script_result` with the handle to block for the result, or "
            f"`check_script_result` to poll without blocking."
        )


async def wait_script_result_text(
    get_client: Callable[[], Awaitable[Client]], handle: str
) -> str:
    """Block until the run_script workflow ``handle`` finishes and return its reply."""
    try:
        client = await get_client()
    except BackendUnavailable as e:
        return _backend_down_text(e)
    try:
        return await client.get_workflow_handle(handle).result()
    except WorkflowFailureError as e:
        return f"Script workflow {handle!r} failed: {e}"


async def check_script_result_text(
    get_client: Callable[[], Awaitable[Client]], handle: str
) -> str:
    """Non-blocking: return the run_script reply if ready, else the workflow's current state."""
    try:
        client = await get_client()
    except BackendUnavailable as e:
        return _backend_down_text(e)
    wf = client.get_workflow_handle(handle)
    desc = await wf.describe()
    if desc.status == WorkflowExecutionStatus.COMPLETED:
        return await wf.result()  # ready — returns immediately
    if desc.status == WorkflowExecutionStatus.RUNNING:
        return (
            f"Script {handle!r} is still running. Poll again with check_script_result, or "
            f"call wait_script_result to block for the result."
        )
    status = desc.status.name if desc.status else "UNKNOWN"
    return f"Script {handle!r} did not complete — workflow status: {status}."


def build_server(
    get_client: Callable[[], Awaitable[Client]], task_queue: str
) -> Server:
    """Build the MCP server.

    ``get_client`` lazily returns a connected Temporal client (raising
    :class:`BackendUnavailable` if the backend isn't reachable); ``task_queue`` is the
    queue the backend's Worker polls. ``run_script`` uses them to start
    :class:`RunScriptWorkflow`. The stdio server owns no server/worker — the backend is run
    separately (see ``durable_mcp_gateway.serve``) so workflows outlive a Claude session.
    """
    server: Server = Server("durable-mcp-gateway")

    # This stdio server acts as one local user (OS process isolation is the trust
    # boundary). It mints an opaque session handle for that user and threads it into
    # the Workflow; the call_tool_activity resolves it to pick the right OAuth token.
    # Cached per process so we don't churn session rows.
    vault = vault_mod.open_default_vault()
    _session: dict[str, str] = {}

    async def local_session_id() -> str:
        if "id" not in _session:
            _session["id"] = await vault.create_session(config.LOCAL_USER_ID)
        return _session["id"]

    run_script_tool = types.Tool(
        name="run_script",
        # The description is the contract the model writes scripts against; mirror RunScript's docstring.
        description=(
            "Durably run a Python script in the pydantic-monty sandbox via a Temporal "
            "Workflow, and get back only what the script returns and prints.\n"
            "\n"
            "DO THE WHOLE TASK IN ONE SCRIPT. When a task spans many tool calls — especially "
            "fanning out over a list (fetch N items, check each, collect the matches) — write "
            "ONE script that does the entire thing: enumerate, loop/gather the calls, and "
            "filter/aggregate INSIDE the script, returning only the final answer. Do NOT call "
            "run_script once per item, and do NOT return raw intermediate data (whole page "
            "bodies, full listings) just to look at it — that pulls everything into your "
            "context and defeats the purpose. Keep the big data in the sandbox; return only "
            "the small result. One run_script call should usually be enough for a whole task.\n"
            "\n"
            "Sandbox: no network/filesystem/ambient I/O (only `import asyncio`, for "
            "concurrency). Ordinary Python works (loops, comprehensions, f-strings, print). "
            "Upstream MCP tools are ASYNC functions, one per tool, called by keyword — you "
            "must `await` them, and should `asyncio.gather(...)` independent calls to run them "
            "CONCURRENTLY (far faster than awaiting one at a time). NOTE: the sandbox's asyncio "
            "is minimal — `gather(*coros)` takes ONLY positional coroutines, no keyword args "
            "(so NO `return_exceptions=True`), and there is no `Semaphore` or `async with`; "
            "gather every call and let a failure raise. Call 'list_upstream_tools' "
            "first for the typed stub of every function; the script is type-checked against it "
            "before running (unknown functions, missing/extra args, wrong types, and a missing "
            "`await` are reported up front). A tool returns the typed result the stub shows, "
            "usually a dict you index with result['key']. When a tool declares no output "
            "schema that type is LEARNED from what past calls returned, so it is incomplete: "
            "indexing a field it does not list is a type error, and result.get('field') is the "
            "way to reach one it has not seen. A learned type does not guarantee the result is "
            "a dict on any given call, so check before indexing. "
            "A tool with no schema and nothing learned yet "
            "returns whatever the upstream sent — a dict, a list, a string, a number, or None "
            "for a plain-text result — so check it before indexing. "
            "A tool FAILURE raises a catchable RuntimeError at its await. The script's LAST "
            "expression is the result, alongside anything it printed.\n"
            "\n"
            "If the script takes longer than ~10s it does NOT block: it returns a `handle` and "
            "a live Temporal UI URL (the script keeps running on the backend). Tell the user "
            "they can watch progress at that URL, then use `wait_script_result` (blocks) or "
            "`check_script_result` (polls) with the handle to get the result.\n"
            "\n"
            "Example — the RIGHT shape for 'which of these pages mention X in the body?': one "
            "script, bodies filtered in the sandbox, only the links come back:\n"
            "    import asyncio\n"
            "    async def main():\n"
            "        rows = (await notion_notion_query_data_sources(data={...}))['results']\n"
            "        docs = await asyncio.gather(*[notion_notion_fetch(id=r['url']) for r in rows])\n"
            "        return [r['url'] for r, d in zip(rows, docs) if 'X' in d['text'].lower()]\n"
            "    asyncio.run(main())"
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "The Python/monty script source to run in the sandbox.",
                },
            },
            "required": ["script"],
        },
    )

    list_upstream_tools_tool = types.Tool(
        name="list_upstream_tools",
        description=(
            "Return a typed Python stub (a .py source string) describing every upstream MCP "
            "tool run_script can call: one keyword-only function per tool, with the tool's "
            "description as the docstring. A tool that declares an output schema has a typed "
            "result — a TypedDict when that schema is an object, otherwise the type the "
            "schema maps to. A tool that declares none gets a TypedDict built from the fields "
            "its past calls returned, which is incomplete by construction: index only the "
            "fields it lists and use result.get('field') for any other. Until such a tool has "
            "returned something, its result is untyped. "
            "Write run_script scripts against these signatures — the script is type-checked "
            "against this stub. "
            "The stub is produced by the durable backend; if it isn't running yet a note is "
            "returned instead. For the raw JSON Schemas use 'list_upstream_tools_as_json'."
        ),
        inputSchema={"type": "object", "properties": {}},
    )

    list_upstream_tools_as_json_tool = types.Tool(
        name="list_upstream_tools_as_json",
        description=(
            "List the upstream MCP tools as raw JSON. Returns {\"tools\": [...]} where each "
            "entry is {name, py_name, py_arg_map, description, input_schema, output_schema}. "
            "Prefer 'list_upstream_tools' (the typed stub) for writing scripts; this is the "
            "underlying schema data. Empty if the durable backend isn't running yet."
        ),
        inputSchema={"type": "object", "properties": {}},
    )

    _HANDLE_SCHEMA = {
        "type": "object",
        "properties": {
            "handle": {
                "type": "string",
                "description": "The handle returned by run_script when it was still running.",
            },
        },
        "required": ["handle"],
    }

    wait_script_result_tool = types.Tool(
        name="wait_script_result",
        description=(
            "Block until a run_script workflow finishes and return its result. Pass the "
            "`handle` that run_script returned when it reported the script was still running. "
            "Use this when you want to wait for the answer."
        ),
        inputSchema=_HANDLE_SCHEMA,
    )

    check_script_result_tool = types.Tool(
        name="check_script_result",
        description=(
            "Non-blocking: return a run_script's result if it's ready, otherwise its current "
            "status (running / failed / …). Pass the `handle` run_script returned. Use this to "
            "poll without blocking."
        ),
        inputSchema=_HANDLE_SCHEMA,
    )

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            run_script_tool,
            wait_script_result_tool,
            check_script_result_tool,
            list_upstream_tools_tool,
            list_upstream_tools_as_json_tool,
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict | None) -> list[types.ContentBlock]:
        if name == "list_upstream_tools":
            text = await list_upstream_tools_text(get_client, task_queue)
            return [types.TextContent(type="text", text=text)]

        if name == "list_upstream_tools_as_json":
            text = await list_upstream_tools_as_json_text(get_client, task_queue)
            return [types.TextContent(type="text", text=text)]

        if name == "run_script":
            # local_session_id mints (once, cached) the opaque session threaded into the
            # Workflow so call_tool_activity can resolve the right OAuth token. The Workflow
            # drives the script's suspend-at-tool-call loop and returns accumulated stdout
            # plus the final expression (or a "Script error (...)" reply — that is data).
            text = await run_script_text(
                get_client,
                task_queue,
                (arguments or {}).get("script"),
                local_session_id,
                wait_seconds=config.RUN_SCRIPT_WAIT_SECONDS,
            )
            return [types.TextContent(type="text", text=text)]

        if name == "wait_script_result":
            handle = (arguments or {}).get("handle") or ""
            text = await wait_script_result_text(get_client, handle)
            return [types.TextContent(type="text", text=text)]

        if name == "check_script_result":
            handle = (arguments or {}).get("handle") or ""
            text = await check_script_result_text(get_client, handle)
            return [types.TextContent(type="text", text=text)]

        raise ValueError(f"unknown tool {name!r}")

    return server
