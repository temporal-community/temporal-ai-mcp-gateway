"""Shared connection config for the durable backend.

Both the backend (``durable_mcp_gateway.serve``) and the stdio server (``stdio.run``)
read these so they agree on where Temporal lives. Overridable via environment.
"""

from __future__ import annotations

import logging
import os
import sys

# gRPC frontend the stdio server connects to and the backend binds.
# Intentionally NOT the standard Temporal dev-server defaults (7233/8233) so running this
# project doesn't collide with an unrelated Temporal dev server on the same machine.
TEMPORAL_ADDRESS = os.environ.get("DURABLE_MCP_GATEWAY_TEMPORAL_ADDRESS", "localhost:7677")
TEMPORAL_NAMESPACE = os.environ.get("DURABLE_MCP_GATEWAY_TEMPORAL_NAMESPACE", "default")
# Web UI port the backend serves.
TEMPORAL_UI_PORT = int(os.environ.get("DURABLE_MCP_GATEWAY_TEMPORAL_UI_PORT", "8677"))

# host/port split out for the backend's start_local (which takes them separately).
_HOST, _, _PORT = TEMPORAL_ADDRESS.partition(":")
TEMPORAL_HOST = _HOST or "127.0.0.1"
TEMPORAL_PORT = int(_PORT) if _PORT else 7677

# Persistent SQLite file for the dev server. Without this, start_local uses ephemeral
# storage and loses all workflow history when it stops — defeating cross-session
# durability. Defaults under the user's home; override with DURABLE_MCP_GATEWAY_DB_PATH.
DB_PATH = os.environ.get(
    "DURABLE_MCP_GATEWAY_DB_PATH",
    os.path.join(os.path.expanduser("~"), ".durable-mcp-gateway", "temporal.db"),
)

# Max activities (upstream tool calls, monty steps, catalog fetches) the Worker runs at once.
# This is what bounds tool-call parallelism: a script can `asyncio.gather` any number of tool
# calls, but only this many execute concurrently — the rest queue. Keeps a fan-out script
# polite to upstreams and the host regardless of how it's written.
MAX_CONCURRENT_ACTIVITIES = int(
    os.environ.get("DURABLE_MCP_GATEWAY_MAX_CONCURRENT_ACTIVITIES", "10")
)

# How long run_script waits inline for a script to finish before handing back a handle + a
# live Temporal UI link (so a long fan-out doesn't block the MCP call). wait_script_result /
# check_script_result then follow the handle.
RUN_SCRIPT_WAIT_SECONDS = float(
    os.environ.get("DURABLE_MCP_GATEWAY_RUN_SCRIPT_WAIT_SECONDS", "10")
)

# How a user starts the backend — surfaced in errors when the stdio server can't reach it.
SERVE_HINT = "uv run durable-mcp-gateway backend"
# The same backend as two processes, so stopping the worker leaves the server and Web UI up.
SERVER_HINT = "uv run durable-mcp-gateway server"
WORKER_HINT = "uv run durable-mcp-gateway worker"
# What to tell a user when the stdio server can't reach the backend. Naming `backend` alone would
# be wrong in the split setup, where the Temporal server is usually up and holding its port.
BACKEND_DOWN_HINT = (
    f"{SERVE_HINT} — or, if you run its halves separately, restart whichever stopped: "
    f"{SERVER_HINT} / {WORKER_HINT}"
)
# How a user authorizes an OAuth upstream — the prefix; the upstream name is appended.
CONNECT_HINT = "uv run durable-mcp-gateway connect"

# --- OAuth token vault ----------------------------------------------------
# Per-(user, upstream) OAuth tokens live in one JSON blob: the OS keychain on
# macOS, a 0600 file elsewhere. The gateway (connect) writes it; the worker's
# call_tool_activity reads/refreshes it. Both run on the same host.
# DURABLE_MCP_GATEWAY_CRED_BACKEND ("keychain"|"file") overrides the platform default.
CRED_BACKEND = os.environ.get("DURABLE_MCP_GATEWAY_CRED_BACKEND") or (
    "keychain" if sys.platform == "darwin" else "file"
)
KEYCHAIN_SERVICE = os.environ.get(
    "DURABLE_MCP_GATEWAY_KEYCHAIN_SERVICE", "durable-mcp-gateway-credentials"
)
CREDENTIALS_PATH = os.environ.get(
    "DURABLE_MCP_GATEWAY_CREDENTIALS_PATH",
    os.path.join(os.path.expanduser("~"), ".durable-mcp-gateway", "credentials.json"),
)

# The single local user the stdio server acts as (no downstream auth — OS
# process isolation is the trust boundary). The vault keys tokens by this id.
LOCAL_USER_ID = "local"

# Loopback redirect for upstream OAuth. The gateway's connect flow listens here;
# the worker's call path never opens a browser, but the MCP SDK still requires a
# registered redirect URI on the client metadata, so both share this value.
OAUTH_CALLBACK_PORT = int(
    os.environ.get("DURABLE_MCP_GATEWAY_OAUTH_CALLBACK_PORT", "41100")
)
OAUTH_CALLBACK_PATH = "/upstream/callback"
OAUTH_REDIRECT_URI = f"http://127.0.0.1:{OAUTH_CALLBACK_PORT}{OAUTH_CALLBACK_PATH}"

# On a headless/remote host, print the authorization URL instead of opening a browser
# (the loopback callback still has to be reachable from wherever you open it).
HEADLESS = os.environ.get("DURABLE_MCP_GATEWAY_HEADLESS") == "1"


# --- logging --------------------------------------------------------------


def configure_logging(verbose: bool = False) -> None:
    """The single logging setup for every CLI command (connect/validate/backend/stdio).

    Quiet by default (WARNING): normal output is just each command's own messages plus real
    warnings (e.g. a per-upstream connect failure). ``-v/--verbose`` opens the INFO firehose
    that's useful for debugging — httpx requests, MCP protocol negotiation, Temporal's
    per-step trace. Always logs to stderr: the stdio server speaks JSON-RPC on stdout, and keeping
    stdout clean also lets ``validate``/``backend`` be piped without log lines mixed in.
    """
    if verbose:
        level, fmt = logging.INFO, "%(asctime)s %(name)s %(levelname)s %(message)s"
    else:
        level, fmt = logging.WARNING, "%(levelname)s %(message)s"
    logging.basicConfig(level=level, format=fmt, stream=sys.stderr, force=True)
