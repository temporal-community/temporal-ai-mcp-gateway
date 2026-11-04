"""The durable backend: a persistent Temporal dev server + the worker.

Run this knowingly in a terminal (``uv run durable-mcp-gateway backend``); it runs in the
FOREGROUND until you Ctrl-C. It is deliberately separate from the stdio MCP server: the
backend must outlive any single Claude session so that a workflow submitted in one session
keeps running and can be queried in the next. The stdio server connects to it as a pure client.

Storage is a persistent SQLite file (see config.DB_PATH), so workflow history survives even
across restarts of this process.

The same two halves also run as separate processes — ``durable-mcp-gateway server`` and
``durable-mcp-gateway worker`` — so the worker can be stopped and restarted (Ctrl-C in its own
terminal) while the Temporal server and its Web UI stay up to show the workflow resuming.
"""

from __future__ import annotations

import asyncio
import os
import signal
from collections.abc import Coroutine

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.testing import WorkflowEnvironment

from . import config, upstreams
from .worker import TASK_QUEUE, new_worker


async def _start_dev_server() -> WorkflowEnvironment:
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    print(
        f"durable-mcp-gateway Temporal server starting: address={config.TEMPORAL_ADDRESS} "
        f"namespace={config.TEMPORAL_NAMESPACE} db={config.DB_PATH} "
        f"(downloads the Temporal binary on first run)...",
        flush=True,
    )
    return await WorkflowEnvironment.start_local(
        namespace=config.TEMPORAL_NAMESPACE,
        data_converter=pydantic_data_converter,
        ip=config.TEMPORAL_HOST,
        port=config.TEMPORAL_PORT,
        ui=True,
        ui_port=config.TEMPORAL_UI_PORT,
        dev_server_database_filename=config.DB_PATH,
    )


def _stop_on_signals() -> asyncio.Event:
    """An Event set on Ctrl-C (SIGINT) or a service manager's SIGTERM, so the caller always
    shuts down through its own cleanup rather than being torn down mid-flight."""
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop.set)
        except NotImplementedError:
            pass
    return stop


async def amain() -> None:
    # Logging is configured by the CLI entry (config.configure_logging); -v surfaces the
    # Temporal per-step trace and discovery's HTTP noise, otherwise this stays quiet.

    # Discover upstreams before serving so call_tool_activity has a populated registry and
    # the stdio server can fetch the catalog over Temporal.
    await upstreams.setup_worker()
    env = await _start_dev_server()
    stop = _stop_on_signals()
    try:
        async with new_worker(env.client):
            print(
                f"durable-mcp-gateway backend ready: Temporal at {config.TEMPORAL_ADDRESS}, "
                f"Web UI http://localhost:{config.TEMPORAL_UI_PORT}, "
                f"worker polling {TASK_QUEUE!r}. Press Ctrl-C to stop.",
                flush=True,
            )
            await stop.wait()
    finally:
        print("durable-mcp-gateway backend shutting down", flush=True)
        await env.shutdown()


async def aserver() -> None:
    """Run the Temporal dev server alone; the worker runs as its own process."""
    env = await _start_dev_server()
    stop = _stop_on_signals()
    try:
        print(
            f"durable-mcp-gateway server ready: Temporal at {config.TEMPORAL_ADDRESS}, "
            f"Web UI http://localhost:{config.TEMPORAL_UI_PORT}. "
            f"Start the worker in another terminal with: {config.WORKER_HINT}",
            flush=True,
        )
        await stop.wait()
    finally:
        print("durable-mcp-gateway server shutting down", flush=True)
        await env.shutdown()


async def aworker() -> None:
    """Run the worker alone against an already-running ``durable-mcp-gateway server``.

    Exits with the command to start that server if it isn't reachable, rather than polling
    an address nothing is listening on.
    """
    try:
        client = await Client.connect(
            config.TEMPORAL_ADDRESS,
            namespace=config.TEMPORAL_NAMESPACE,
            data_converter=pydantic_data_converter,
        )
        await client.service_client.check_health()
    except Exception as e:  # noqa: BLE001 - any connect failure means "server not up"
        raise SystemExit(
            f"durable-mcp-gateway worker: no Temporal server at {config.TEMPORAL_ADDRESS} "
            f"({e}). Start it in another terminal with:\n    {config.SERVER_HINT}"
        )

    await upstreams.setup_worker()
    stop = _stop_on_signals()
    async with new_worker(client):
        print(
            f"durable-mcp-gateway worker ready: polling {TASK_QUEUE!r} at "
            f"{config.TEMPORAL_ADDRESS}. Press Ctrl-C to stop.",
            flush=True,
        )
        await stop.wait()
    print("durable-mcp-gateway worker stopped", flush=True)


def _run(coro: Coroutine[object, object, None]) -> None:
    try:
        asyncio.run(coro)
    except KeyboardInterrupt:
        pass  # SIGINT without a handler (e.g. off the main thread) — exit quietly.


def main() -> None:
    _run(amain())


def server_main() -> None:
    _run(aserver())


def worker_main() -> None:
    _run(aworker())


if __name__ == "__main__":
    # Direct invocation bypasses the CLI's logging setup, so do the quiet default here.
    config.configure_logging()
    main()
