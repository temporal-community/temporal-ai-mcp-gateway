"""Entry point: run the MCP server over stdio.

The stdio server is a pure CLIENT of the durable backend (Temporal server + worker). The backend
is run separately and outlives any Claude session — start it with ``uv run
durable-mcp-gateway backend`` (see ``durable_mcp_gateway.serve``). This process only exposes MCP
tools over stdio and submits/queries workflows; it owns no server and leaves nothing
running on exit. If the backend isn't up, the stdio server still starts and ``run_script``
returns an actionable message rather than failing to launch.
"""

from __future__ import annotations

import asyncio
import sys

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from mcp.server.stdio import stdio_server

from durable_mcp_gateway import config
from durable_mcp_gateway.worker import TASK_QUEUE

from .server import BackendUnavailable, build_server


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


async def run_local() -> None:
    # Logging is configured by the CLI entry (config.configure_logging), always to stderr so
    # stdout stays a clean JSON-RPC channel; -v surfaces the INFO detail.
    server = build_server(get_client, TASK_QUEUE)
    _log(
        f"MCP over stdio; durable backend expected at {config.TEMPORAL_ADDRESS} "
        f"(task_queue={TASK_QUEUE}). Run `{config.SERVE_HINT}` if it isn't up."
    )
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


def main() -> None:
    asyncio.run(run_local())


if __name__ == "__main__":
    # Direct invocation bypasses the CLI's logging setup, so do the quiet default here.
    config.configure_logging()
    main()
