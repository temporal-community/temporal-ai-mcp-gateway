"""``connect``: authorize an OAuth upstream out of band, writing its token to the vault.

    uv run durable-mcp-gateway connect <upstream-name>

A short-lived process: it opens the browser, runs the OAuth authorization-code+PKCE
handshake against the upstream, catches the redirect on a loopback HTTP server, and
persists the resulting token to the vault under (local user, upstream). Then exit.

This is the out-of-band setup step — the human connects their accounts once, like
enabling an integration. The durable backend picks the token up at discovery (start
it after connecting, or restart it), and ``call_tool_activity`` uses it per call. The
PKCE verifier and tokens never leave this process / the vault; only the authorization
URL is opened in the browser.
"""

from __future__ import annotations

import asyncio
import sys

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.routing import Route

from mcp import ClientSession
from mcp.client.auth import OAuthClientProvider
from mcp.client.streamable_http import streamablehttp_client

from . import config, upstreams
from .vault import open_default_vault


async def _authorize(server_cfg: dict) -> None:
    """Run the browser OAuth handshake for one upstream and vault the token."""
    name = server_cfg["name"]
    vault = open_default_vault()
    loop = asyncio.get_running_loop()
    # Resolved by the loopback callback with (code, state) once the user approves.
    code_future: asyncio.Future[tuple[str, str | None]] = loop.create_future()

    async def redirect_handler(auth_url: str) -> None:
        if config.HEADLESS:
            print(
                f"Open this URL to authorize {name!r} (then the flow completes here):\n  {auth_url}",
                file=sys.stderr,
            )
            return
        print(f"Opening your browser to authorize {name!r}:\n  {auth_url}", file=sys.stderr)
        import webbrowser

        webbrowser.open(auth_url)

    async def callback_handler() -> tuple[str, str | None]:
        return await code_future

    async def _callback(request: Request) -> Response:
        params = request.query_params
        error = params.get("error")
        if not code_future.done():
            if error:
                code_future.set_exception(RuntimeError(f"upstream returned error={error!r}"))
            else:
                code_future.set_result((params.get("code", ""), params.get("state")))
        if error:
            return HTMLResponse(f"Authorization failed: {error}", status_code=400)
        return HTMLResponse("Authorized. You can close this tab and return to the terminal.")

    app = Starlette(routes=[Route(config.OAUTH_CALLBACK_PATH, _callback, methods=["GET"])])
    server = uvicorn.Server(
        uvicorn.Config(
            app, host="127.0.0.1", port=config.OAUTH_CALLBACK_PORT, log_level="warning"
        )
    )
    server_task = asyncio.create_task(server.serve())
    try:
        provider = OAuthClientProvider(
            server_url=server_cfg["url"],
            client_metadata=upstreams.oauth_client_metadata(server_cfg),
            storage=vault.storage_for(config.LOCAL_USER_ID, name),
            redirect_handler=redirect_handler,
            callback_handler=callback_handler,
        )
        # Initializing a session drives the full flow: discovery -> register ->
        # redirect_handler (browser) -> callback_handler (await approval) -> token
        # exchange -> written to the vault. One round-trip is enough; then close.
        async with streamablehttp_client(url=server_cfg["url"], auth=provider) as (r, w, _):
            async with ClientSession(r, w) as session:
                await session.initialize()
        print(
            f"Connected {name!r}: token stored for user {config.LOCAL_USER_ID!r}. "
            "Restart the backend (or start it now) so discovery includes its tools.",
            file=sys.stderr,
        )
    finally:
        server.should_exit = True
        await server_task


def connect(upstream: str) -> None:
    """Authorize one OAuth upstream by name (from upstreams.json) and vault its token."""
    servers = {s["name"]: s for s in upstreams.load_servers()}
    cfg = servers.get(upstream)
    if cfg is None:
        raise SystemExit(
            f"unknown upstream {upstream!r}; known: {sorted(servers) or '(none configured)'}"
        )
    if not upstreams.is_oauth(cfg):
        raise SystemExit(
            f"upstream {upstream!r} is not OAuth (needs auth.type=='oauth'); nothing to connect"
        )
    if cfg.get("transport") != "streamable-http":
        raise SystemExit("OAuth connect requires the streamable-http transport")

    asyncio.run(_authorize(cfg))
