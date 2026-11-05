"""Entry points: run the MCP server over stdio, or over streamable HTTP.

By default the server is a pure CLIENT of the durable backend (Temporal server + worker). The
backend is run separately and outlives any Claude session — start it with ``uv run
durable-mcp-gateway backend`` (see ``durable_mcp_gateway.serve``). This process only exposes MCP
tools and submits/queries workflows; it owns no server and leaves nothing running on exit. If
the backend isn't up, the server still starts and ``run_script`` returns an actionable message
rather than failing to launch.

With ``no_temporal`` it never connects to Temporal: it discovers the upstreams itself, the way
the backend does, and runs each script in this process, so exiting loses every run in flight.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import signal
import sys
from collections.abc import Callable

import uvicorn
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.routing import Mount
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from mcp.server.stdio import stdio_server

from durable_mcp_gateway import config, upstreams
from durable_mcp_gateway.worker import TASK_QUEUE

from .server import BackendUnavailable, build_no_temporal_server, build_server


def _log(msg: str) -> None:
    # stdout is the MCP JSON-RPC channel — every diagnostic MUST go to stderr.
    print(f"[durable-mcp-gateway] {msg}", file=sys.stderr, flush=True)


_client: Client | None = None


async def get_client() -> Client:
    """Return a healthy client to the durable backend, (re)connecting as needed.

    Caches the connection but health-checks it each call, so a backend that was restarted
    (or started after the stdio server) is picked up transparently. Raises
    :class:`BackendUnavailable` if the backend can't be reached.
    """
    global _client
    if _client is not None:
        try:
            await _client.service_client.check_health()
            return _client
        except Exception:  # noqa: BLE001 - stale connection; drop it and reconnect below
            _client = None
    try:
        client = await Client.connect(
            config.TEMPORAL_ADDRESS,
            namespace=config.TEMPORAL_NAMESPACE,
            data_converter=pydantic_data_converter,
        )
        await client.service_client.check_health()
    except Exception as e:  # noqa: BLE001 - report as a clean "backend down" signal
        raise BackendUnavailable(str(e)) from e
    _client = client
    return client


async def _build(
    no_temporal: bool, progress: Callable[[str], None] | None = None
) -> tuple[Server, str]:
    """The MCP server for the mode, and a note on where its scripts run."""
    if not no_temporal:
        note = (
            f"durable backend expected at {config.TEMPORAL_ADDRESS} "
            f"(task_queue={TASK_QUEUE}). Run `{config.SERVE_HINT}` if it isn't up."
        )
        return build_server(get_client, TASK_QUEUE), note
    report = await upstreams.setup_worker()
    note = (
        f"no Temporal: scripts run in this process against "
        f"{sum(report.connected.values())} tool(s) from {len(report.connected)} upstream(s)."
    )
    return build_no_temporal_server(progress), note


async def run_local(no_temporal: bool = False) -> None:
    # Logging is configured by the CLI entry (config.configure_logging), always to stderr so
    # stdout stays a clean JSON-RPC channel; -v surfaces the INFO detail.
    server, note = await _build(no_temporal)
    _log(f"MCP over stdio; {note}")
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


class _ExitWhereItStands(uvicorn.Server):
    """uvicorn that exits on Ctrl-C/SIGTERM at once, saying the in-flight work is lost.

    A graceful drain would wait for the running scripts to finish instead of losing them.
    """

    @contextlib.contextmanager
    def capture_signals(self):
        def die(signum, frame):
            _log("killed — in-flight work is lost.")
            os._exit(128 + signum)

        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, die)
        yield


async def run_http(port: int, no_temporal: bool = False) -> None:
    server, note = await _build(no_temporal, progress=_log)
    # The SDK's DNS-rebinding protection for a loopback server, as FastMCP applies it.
    manager = StreamableHTTPSessionManager(
        app=server,
        security_settings=TransportSecuritySettings(
            allowed_hosts=["127.0.0.1:*", "localhost:*", "[::1]:*"],
            allowed_origins=["http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*"],
        ),
    )

    @contextlib.asynccontextmanager
    async def lifespan(_app):
        async with manager.run():
            yield

    # Mounted at the root: the transport ignores the path, and a Mount("/mcp") would only
    # match "/mcp/", bouncing a bare "/mcp" through a redirect.
    app = Starlette(routes=[Mount("/", app=manager.handle_request)], lifespan=lifespan)
    _log(f"MCP over streamable-http at http://127.0.0.1:{port}/mcp; {note}")
    uv_config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    await (_ExitWhereItStands if no_temporal else uvicorn.Server)(uv_config).serve()


def main(no_temporal: bool = False) -> None:
    asyncio.run(run_local(no_temporal))


def http_main(port: int, no_temporal: bool = False) -> None:
    try:
        asyncio.run(run_http(port, no_temporal))
    except KeyboardInterrupt:
        pass  # uvicorn re-raises the Ctrl-C it shut down on.


if __name__ == "__main__":
    # Direct invocation bypasses the CLI's logging setup, so do the quiet default here.
    config.configure_logging()
    main()
