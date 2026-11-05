"""The ``durable-mcp-gateway`` command: one entry point for the system's three processes.

    durable-mcp-gateway connect <upstream>   authorize an OAuth upstream once (browser),
                                             storing its token in the vault
    durable-mcp-gateway validate             run the backend's startup discovery without
                                             starting anything: connect every upstream, list
                                             its tools, and check auth
    durable-mcp-gateway call-tool <name>     call a gateway MCP tool by its exact name against
                                             the backend and print its output (the agent's view):
                                               call-tool list_upstream_tools
                                               call-tool list_upstream_tools_as_json
                                               call-tool run_script <path to .py file>
    durable-mcp-gateway backend              run the durable backend (Temporal dev server +
                                             worker); long-lived, outlives Claude sessions
    durable-mcp-gateway server               run the backend's Temporal dev server alone
    durable-mcp-gateway worker               run the backend's worker alone, against a running
                                             `server`; Ctrl-C stops it without taking the
                                             Temporal server and its Web UI down
    durable-mcp-gateway stdio                run the MCP server over stdio; a pure client of
                                             the backend (this is what Claude spawns)
    durable-mcp-gateway http [--port N]      run the same MCP server over streamable HTTP at
                                             http://127.0.0.1:N/mcp (default 9677), as a
                                             long-lived process you can watch and kill
    durable-mcp-gateway seed-demo --parent <page-url>
                                             create the demo 1-pager database from
                                             examples/demo-db under a Notion page and print
                                             its data source URL

`stdio` and `http` both take --no-temporal: discover the upstreams and run each script in that
process, with no backend, no retries, and nothing surviving the process. This is code mode
without Temporal, for comparing against the durable default.

Typical order: `connect` your upstreams once, run `backend` in its own terminal, then point
your MCP client at `stdio`. See the module docstrings in ``connect_cli``, ``serve``, and
``stdio.run`` for the details of each.

Subcommand implementations are imported lazily so that, e.g., the stdio and http servers don't
import ``serve`` (the backend, with its Temporal dev-server deps) or ``connect_cli``.
"""

from __future__ import annotations

import argparse
import asyncio
import sys


def _validate() -> None:
    """Run the backend's startup discovery and report, without starting the backend.

    This calls ``upstreams.setup_worker()`` — the *same* bootstrap the backend runs before
    it launches Temporal (see :mod:`.serve`) — so validate can never drift from what startup
    actually enforces: it connects every configured upstream, registers its tools, and
    hard-fails (RuntimeError) on an unauthorized OAuth upstream. Unlike the backend, which
    *degrades* past a per-upstream connect failure so one flaky upstream can't block startup,
    validate is a strict pre-flight check: any upstream that failed to connect (reported in
    the DiscoveryReport) is a validation failure too.
    Exit 0 only if every configured upstream connected; otherwise exit 1.
    """
    from . import upstreams

    configured = [s["name"] for s in upstreams.load_servers()]
    print(
        f"Validating {len(configured)} upstream(s) from {upstreams.UPSTREAMS_PATH} ...",
        flush=True,
    )
    try:
        report = asyncio.run(upstreams.setup_worker())
    except RuntimeError as e:
        print(f"\nValidation FAILED:\n{e}", file=sys.stderr)
        raise SystemExit(1)

    failed = dict(report.failed)
    for name in configured:
        if name in failed:
            print(f"  ✗ {name}: FAILED to connect — {failed[name]}")
        else:
            count = report.connected.get(name, 0)
            print(f"  ✓ {name}: {count} tool(s)")
    sys.stdout.flush()  # keep the per-upstream lines ahead of any stderr verdict below

    if failed:
        print(
            f"\nValidation FAILED: {len(failed)} of {len(configured)} upstream(s) "
            "could not be connected (see above).",
            file=sys.stderr,
        )
        raise SystemExit(1)

    total = sum(report.connected.values())
    print(f"\nValidation OK: {total} tool(s) across {len(configured)} upstream(s).")


def _call_tool(tool: str, script_path: str | None = None, command: str | None = None) -> None:
    """Call one stdio-server MCP tool by its exact name against the backend and print its output.

    Thin wrappers over the *same* module-level functions the stdio server's call_tool handler
    uses (stdio.server), so the output is byte-identical to what an MCP client / the agent would
    receive — including the "backend not reachable" fallbacks. run_script's source comes from
    a .py file path or a literal -c string (like python), and mints its own opaque session (as
    the stdio server does per client).
    """
    import pathlib

    from stdio import server
    from stdio.run import get_client
    from . import config, vault as vault_mod
    from .worker import TASK_QUEUE

    if tool == "run_script":
        if command is not None and script_path is not None:
            raise SystemExit("call-tool run_script: give a file path OR -c, not both")
        if command is not None:
            script = command
        elif script_path is not None:
            try:
                script = pathlib.Path(script_path).read_text()
            except OSError as e:
                raise SystemExit(f"cannot read script {script_path!r}: {e}")
        else:
            raise SystemExit("call-tool run_script requires a .py file path or -c <script>")

        async def session_provider() -> str:
            return await vault_mod.open_default_vault().create_session(config.LOCAL_USER_ID)

        print(asyncio.run(server.run_script_text(get_client, TASK_QUEUE, script, session_provider)))
        return

    # The listing tools take no arguments.
    if script_path or command is not None:
        raise SystemExit(f"call-tool {tool} takes no arguments")
    render = {
        "list_upstream_tools": server.list_upstream_tools_text,
        "list_upstream_tools_as_json": server.list_upstream_tools_as_json_text,
    }[tool]
    print(asyncio.run(render(get_client, TASK_QUEUE)))


def main() -> None:
    from . import config

    ap = argparse.ArgumentParser(
        prog="durable-mcp-gateway",
        description="Durable MCP gateway: connect upstreams, run the backend, run the stdio server.",
    )
    # Every subcommand shares -v so logging is configured one way, in one place (below).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-v", "--verbose", action="store_true",
        help="show debug logging (HTTP requests, MCP protocol negotiation, Temporal trace)",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    c = sub.add_parser(
        "connect", parents=[common],
        help="authorize an OAuth upstream (from upstreams.json) and vault its token",
    )
    c.add_argument("upstream", help="name of an auth.type=='oauth' upstream in upstreams.json")

    sub.add_parser(
        "validate", parents=[common],
        help="run the backend's startup discovery and check auth",
    )
    ct = sub.add_parser(
        "call-tool", parents=[common],
        help="call a stdio-server MCP tool by name against the backend and print its output",
    )
    ct.add_argument(
        "tool",
        choices=[
            "list_upstream_tools",
            "list_upstream_tools_as_json",
            "run_script",
        ],
        help="the MCP tool to call (matches the stdio server's tool names)",
    )
    ct.add_argument(
        "script", nargs="?", metavar="SCRIPT.py",
        help="for run_script: path to a .py file whose contents are run in the sandbox",
    )
    ct.add_argument(
        "-c", metavar="SCRIPT", dest="code",
        help="for run_script: literal script source to run, instead of a file path (like python -c)",
    )
    sub.add_parser(
        "backend", parents=[common],
        help="run the durable backend (Temporal dev server + worker); long-lived",
    )
    sub.add_parser(
        "server", parents=[common],
        help="run only the backend's Temporal dev server (worker runs separately)",
    )
    sub.add_parser(
        "worker", parents=[common],
        help="run only the backend's worker, against a running `durable-mcp-gateway server`",
    )
    mode = argparse.ArgumentParser(add_help=False)
    mode.add_argument(
        "--no-temporal", action="store_true",
        help="run scripts in this process instead of on the backend: no Temporal, no retries, "
        "and stopping the process loses any script still running",
    )
    sub.add_parser(
        "stdio", parents=[common, mode],
        help="run the MCP server over stdio (a backend client, unless --no-temporal)",
    )
    h = sub.add_parser(
        "http", parents=[common, mode],
        help="run the MCP server over streamable HTTP at http://127.0.0.1:PORT/mcp",
    )
    h.add_argument("--port", type=int, default=9677, help="port to listen on (default 9677)")
    sd = sub.add_parser(
        "seed-demo", parents=[common],
        help="create the demo 1-pager database (examples/demo-db) under a Notion page",
    )
    sd.add_argument(
        "--parent", required=True, metavar="PAGE_URL",
        help="the Notion page to create the database under; uses the `connect notion` login",
    )

    args = ap.parse_args()
    config.configure_logging(verbose=args.verbose)

    if args.command == "connect":
        from .connect_cli import connect

        connect(args.upstream)
    elif args.command == "validate":
        _validate()
    elif args.command == "call-tool":
        _call_tool(args.tool, args.script, args.code)
    elif args.command == "backend":
        from .serve import main as backend_main

        backend_main()
    elif args.command == "server":
        from .serve import server_main

        server_main()
    elif args.command == "worker":
        from .serve import worker_main

        worker_main()
    elif args.command == "stdio":
        from stdio.run import main as stdio_main

        stdio_main(args.no_temporal)
    elif args.command == "http":
        from stdio.run import http_main

        http_main(args.port, args.no_temporal)
    elif args.command == "seed-demo":
        from .seed_demo import seed_demo

        seed_demo(args.parent)


if __name__ == "__main__":
    main()
