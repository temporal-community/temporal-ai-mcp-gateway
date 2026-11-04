"""Tests for the OAuth session/vault threading and the connect CLI validation.

The live browser handshake isn't automated (it needs a human to approve), but every
non-interactive seam is covered: the vault, the activity's session->user->token
resolution, and the CLI's up-front validation.
"""

import json
import os

import pytest
from mcp.shared.auth import OAuthToken

from durable_mcp_gateway import config, connect_cli, upstreams
from durable_mcp_gateway.activities import call_tool_activity
from durable_mcp_gateway.models import CallToolRequest
from durable_mcp_gateway.vault import FileCredentialStore, JsonVault


def _use_file_vault(tmp_path, monkeypatch):
    """Point the default vault at a temp file (config is read at call time, and its
    module constants are import-time, so patch the attributes — not the env)."""
    monkeypatch.setattr(config, "CRED_BACKEND", "file")
    monkeypatch.setattr(config, "CREDENTIALS_PATH", str(tmp_path / "creds.json"))


# --- vault ----------------------------------------------------------------


async def test_vault_session_and_token_roundtrip(tmp_path):
    path = str(tmp_path / "credentials.json")
    vault = JsonVault(FileCredentialStore(path))

    # A session handle resolves to a user; two sessions for one user share a row.
    s1 = await vault.create_session("local")
    s2 = await vault.create_session("local")
    assert s1 != s2
    assert vault.user_for_session(s1) == "local"
    with pytest.raises(KeyError):
        vault.user_for_session("nope")

    slot = vault.storage_for("local", "notion")
    assert await slot.get_tokens() is None

    await slot.set_tokens(
        OAuthToken(access_token="a1", refresh_token="r1", expires_in=3600)
    )
    toks = await slot.get_tokens()
    assert toks is not None and toks.access_token == "a1"

    # 0600 + persistence: a fresh vault on the same file sees session + token.
    assert (os.stat(path).st_mode & 0o777) == 0o600
    reopened = JsonVault(FileCredentialStore(path))
    assert reopened.user_for_session(s1) == "local"
    toks = await reopened.storage_for("local", "notion").get_tokens()
    assert toks is not None and toks.refresh_token == "r1"


async def test_oauth_provider_primes_expiry_from_vault(tmp_path):
    """Regression: the SDK only tracks token expiry in memory and never restores it on load,
    so a freshly-built provider would deem a loaded-but-expired token valid, skip the refresh,
    and force a needless reconnect. _oauth_provider must re-prime token_expiry_time from the
    vault's stored absolute expires_at."""
    vault = JsonVault(FileCredentialStore(str(tmp_path / "creds.json")))
    slot = vault.storage_for("local", "notion")
    await slot.set_tokens(
        OAuthToken(access_token="a1", refresh_token="r1", expires_in=3600)
    )
    stored = slot.stored_expiry()
    assert stored is not None

    cfg = {
        "name": "notion",
        "transport": "streamable-http",
        "url": "https://example.test/mcp",
        "auth": {"type": "oauth"},
    }
    provider = upstreams._oauth_provider(cfg, slot)
    assert provider.context.token_expiry_time == stored


# --- activity: OAuth upstream with no usable session ----------------------


async def test_call_tool_activity_oauth_without_session_errors(tmp_path, monkeypatch):
    # Point the vault at an empty temp file and register one OAuth-backed tool.
    _use_file_vault(tmp_path, monkeypatch)
    monkeypatch.setattr(
        upstreams, "_REGISTRY",
        {
            "notion_search": upstreams.UpstreamTool(
                namespaced_name="notion.search",
                server_name="notion",
                tool_name="search",
                description="",
                input_schema={},
                output_schema={"type": "object"},
                server_cfg={
                    "name": "notion",
                    "transport": "streamable-http",
                    "url": "https://mcp.notion.com/mcp",
                    "auth": {"type": "oauth"},
                },
                py_name="notion_search",
                py_arg_map={},
            )
        },
    )
    # session_id is empty (unknown) -> resolves to no user -> clear reconnect error,
    # and crucially we never reach the network.
    result = await call_tool_activity(
        CallToolRequest(name="notion_search", arguments={}, session_id="")
    )
    assert result.ok is False
    assert "connect" in result.error.lower()


# --- connect CLI validation ------------------------------------------------


def _write_upstreams(home, servers):
    (home / "upstreams.json").write_text(json.dumps({"servers": servers}))


def test_connect_cli_unknown_upstream(tmp_path, monkeypatch):
    monkeypatch.setattr(upstreams, "UPSTREAMS_PATH", str(tmp_path / "upstreams.json"))
    _write_upstreams(tmp_path, [{"name": "fs", "transport": "stdio", "command": "x"}])
    with pytest.raises(SystemExit, match="unknown upstream"):
        connect_cli.connect("does-not-exist")


def test_connect_cli_non_oauth_upstream(tmp_path, monkeypatch):
    monkeypatch.setattr(upstreams, "UPSTREAMS_PATH", str(tmp_path / "upstreams.json"))
    _write_upstreams(tmp_path, [{"name": "fs", "transport": "stdio", "command": "x"}])
    with pytest.raises(SystemExit, match="not OAuth"):
        connect_cli.connect("fs")


# --- discovery hard-fails on an unauthorized OAuth upstream ----------------


async def test_discover_hard_fails_on_unauthorized_oauth(tmp_path, monkeypatch):
    _use_file_vault(tmp_path, monkeypatch)
    monkeypatch.setattr(upstreams, "UPSTREAMS_PATH", str(tmp_path / "upstreams.json"))
    _write_upstreams(
        tmp_path,
        [{"name": "notion", "transport": "streamable-http",
          "url": "https://mcp.notion.com/mcp", "auth": {"type": "oauth"}}],
    )
    upstreams._REGISTRY.clear()

    # Realistic shape: the MCP client's task group wraps ReconnectRequired in an
    # ExceptionGroup, so discovery must still recognize it and hard-fail.
    async def _raise(server_cfg, token_storage=None):
        raise ExceptionGroup(
            "unhandled errors in a TaskGroup",
            [upstreams.ReconnectRequired("needs authorization")],
        )

    monkeypatch.setattr(upstreams, "_discover_one", _raise)

    with pytest.raises(RuntimeError, match="not authorized"):
        await upstreams.discover_upstreams()
    upstreams._REGISTRY.clear()


def test_find_reconnect_unwraps_exception_group():
    rr = upstreams.ReconnectRequired("x")
    assert upstreams.find_reconnect(rr) is rr
    assert upstreams.find_reconnect(ExceptionGroup("g", [ValueError("v"), rr])) is rr
    # Nested groups too.
    assert upstreams.find_reconnect(ExceptionGroup("g", [ExceptionGroup("h", [rr])])) is rr
    assert upstreams.find_reconnect(ValueError("v")) is None
