# durable-mcp-gateway

An MCP server that durably runs sandboxed Python scripts via Temporal.

The stdio server (`stdio/`) exposes MCP tools. Its `run_script` tool starts a
`RunScriptWorkflow` (`durable_mcp_gateway/`) that runs a user-supplied script inside the
[pydantic-monty](https://pypi.org/project/pydantic-monty/) sandbox — no imports, network,
or filesystem. Upstream MCP tools are exposed as ordinary Python functions (one per tool);
calling one suspends the sandbox and runs a durable Temporal Activity, so every tool call is
a retryable step that survives Worker restarts. The script is statically type-checked against
a generated stub of those functions before it runs, and a tool failure raises a catchable
exception. The tools proxy real upstream MCP servers configured in `upstreams.json` (see below).

## Architecture: two processes

The work is split so that workflows can outlive any single Claude session:

- **The durable backend** (`durable_mcp_gateway.serve`) — a persistent Temporal dev server
  plus the Worker. You run this knowingly in a terminal; it stays up across Claude sessions
  and uses a persistent DB, so a workflow started in one session keeps running and can be
  queried later.
- **The stdio server** (`durable-mcp-gateway stdio`) — the MCP server. It is a pure *client*
  of the backend: it submits/queries workflows and owns no server or worker, so it leaves
  nothing running when Claude exits. If the backend isn't up, it still starts and
  `run_script` returns an actionable message.

## Run

You need [uv](https://docs.astral.sh/uv/) (the Temporal binary is downloaded automatically
on first run of the backend).

```bash
uv sync
```

Copy the example upstream config (a Notion setup) into place:

```bash
mkdir -p ~/.durable-mcp-gateway && cp examples/upstreams.json ~/.durable-mcp-gateway/
```

1. Authorize each OAuth upstream once — opens your browser and stores the token
   (macOS Keychain, else a `0600` file). Do this **before** starting the backend
   (a configured-but-unauthorized OAuth upstream makes it hard-fail at startup):

   ```bash
   uv run durable-mcp-gateway connect notion
   ```

   Optionally, confirm the config is good before starting anything — this runs the
   backend's exact startup discovery (connect every upstream, list its tools, check auth)
   and reports, without launching Temporal:

   ```bash
   uv run durable-mcp-gateway validate
   ```

2. Start the durable backend in a terminal and leave it running:

   ```bash
   uv run durable-mcp-gateway backend
   ```

   It serves Temporal on `localhost:7677` and the Web UI at http://localhost:8677.
   Ctrl-C to stop.

   The backend's two halves can also run as separate processes, one per terminal, so that
   stopping the worker leaves Temporal and its Web UI up — useful for watching an in-flight
   workflow survive a worker restart:

   ```bash
   uv run durable-mcp-gateway server   # Temporal + Web UI
   uv run durable-mcp-gateway worker   # the worker alone; Ctrl-C stops just this
   ```

   `worker` exits with the command to start `server` if it isn't reachable. Workflow history
   lives in the same persistent DB either way, so a workflow that was running when the worker
   stopped picks up where it left off once the worker is back.

3. Register the stdio server with Claude Code:

   ```bash
   claude mcp add gateway --scope user -- uv --directory $(pwd) run durable-mcp-gateway stdio
   ```

4. Restart Claude Code and try prompting:

   - `call gateway:list_upstream_tools` to get the typed stub of the upstream tools you can call
   - `use gateway:run_script to run: import asyncio; asyncio.run(notion_notion_get_users(page_size=3))`

To exercise the stdio server's MCP tools from the shell (handy for debugging what the model sees),
`call-tool` invokes one by its exact name against the running backend and prints its output —
byte-identical to the MCP tool call, since it's a thin wrapper over the same code:

```bash
uv run durable-mcp-gateway call-tool list_upstream_tools           # the typed stub
uv run durable-mcp-gateway call-tool list_upstream_tools_as_json   # the raw JSON catalog
uv run durable-mcp-gateway call-tool run_script path/to/script.py  # run a script in the sandbox
uv run durable-mcp-gateway call-tool run_script -c 'import asyncio; asyncio.run(notion_notion_get_users(page_size=1))'  # literal source
```

For a fuller example of *why* the gateway is useful, see
`examples/notion_find_1pagers_mentioning_ai.py`: it scans a Notion database and returns only
the 1-pagers whose **body** mentions AI/agents. The page bodies are read and filtered inside
the sandbox, so the model's context gets just the short list of matching links — not the
dozens of full pages a direct-MCP agent would have to read to filter on body text.

## Upstream MCP tools

Upstream MCP servers are configured in `~/.durable-mcp-gateway/upstreams.json`; the backend
connects to each at startup, lists its tools, and registers them. Each tool is exposed to a
script as a Python function whose name is the namespaced `<server>.<tool>` sanitized to a
valid identifier (e.g. `fixture.add` → `fixture_add`, `github-mcp.create-issue` →
`github_mcp_create_issue`), with one keyword argument per input-schema property. The functions
are async, so a script calls `await fixture_add(a=1, b=2)`. See `examples/upstreams.json` for
the config shape — `stdio` servers need a `command` (plus optional `args`/`env`),
`streamable-http` servers need a `url` (plus optional static `headers`). `${ENV}` references
in any value are expanded from the backend's environment.

A tool that declares an `outputSchema` is typed from it. Many upstream tools declare none;
such a tool is typed from what it has actually been seen to return. Every successful call — to
any tool — contributes the field names and broad types it came back with, never the values,
merged across calls and cached in `~/.durable-mcp-gateway/upstreams-shapes.json`, so what a
tool was seen to return survives a backend restart. A result keyed by data rather than by a
fixed set of fields would store those keys as field names, so a tool whose merged shape passes
64 fields has that shape discarded and is never learned from again.

That learned shape becomes the function's return type in the stub, a TypedDict with the fields
past calls returned. Because it is a union over those calls and nothing more, it is incomplete
by construction, and `run_script` type-checks against it before running: indexing a field the
type doesn't list fails the check even when the script is correct. `result.get("field")` is
the way to reach a field that hasn't been seen, and the generated docstring says so. A tool
with neither a schema nor an observed result keeps an untyped result. A server's `"skip"` list
drops a tool from the catalog altogether.

The catalog itself lives only in the backend's in-memory registry; the stdio server fetches it
over Temporal. Its `list_upstream_tools` serves a rendered typed Python stub (a model writes
scripts against it; `run_script` type-checks against it); `list_upstream_tools_as_json` serves
the raw catalog JSON.

### Upstream auth

An `auth` block on a `streamable-http` upstream selects how it authenticates:

- **static/bearer** — put credentials in `headers` (e.g. `"X-API-Key": "${KEY}"`).
- **OAuth** — `"auth": { "type": "oauth" }`. Authorize it out of band once with
  `uv run durable-mcp-gateway connect <server>`: that runs the browser OAuth flow and stores
  the token in the vault (macOS Keychain, else a `0600` file) per local user and upstream.
  Discovery and every tool call then use that token, refreshing it transparently. A
  configured OAuth upstream with no stored token makes the backend **hard-fail at startup**
  with the connect command to run. (The token is threaded to tool calls via an opaque
  session id: stdio server → `RunScriptWorkflow` → `call_tool_activity`, which resolves it to
  the user and reads the vault — the sandbox/Workflow never sees the token.)

### Environment overrides

- `DURABLE_MCP_GATEWAY_TEMPORAL_ADDRESS` (default `localhost:7677`) — intentionally not
  the standard Temporal ports (7233/8233) to avoid colliding with an unrelated dev server.
- `DURABLE_MCP_GATEWAY_TEMPORAL_NAMESPACE` (default `default`)
- `DURABLE_MCP_GATEWAY_TEMPORAL_UI_PORT` (default `8677`)
- `DURABLE_MCP_GATEWAY_DB_PATH` (default `~/.durable-mcp-gateway/temporal.db`) — the backend's
  persistent storage.

## Debugging the workflow

To iterate on the durable workflow alone (no MCP/stdio layer), run a script straight
through `RunScriptWorkflow`. Auto-starts the backend if it isn't already running:

```bash
uv run python scripts/run_workflow.py 'xs = [i * i for i in range(5)]; print(f"squares: {xs}"); sum(xs)'
```

## Tests

```bash
uv run pytest tests/ -v
```

The tests run the Workflow against a `WorkflowEnvironment` + `Worker`, exercising the real
durable suspend/resume path without a separately running server.
