"""The vault: opaque session handles + per-(user, upstream) OAuth tokens.

Ported from the `donald/oauth-local` prototype. Two responsibilities, one JSON
document:

  sessions   session_id -> user_id            the opaque handle the gateway mints
  tokens     (user_id, upstream) -> {token, client_info, expires_at}

The gateway mints a `session_id` (resolving to a user) and threads it through the
Workflow as input; the `call_tool_activity` is handed that session_id and resolves
it to a user to find the token. Tokens are keyed by *user*, not session, so
multiple sessions for the same user share — and refresh — the same row.

Persisted to the **OS keychain on macOS** and a **0600 file** elsewhere, mirroring
how Claude Code stores MCP OAuth credentials. `TokenVault` is the seam; `JsonVault`
is the only implementation, parameterized by a `CredentialStore` (keychain vs file).

Known limitations (both to be resolved by moving to a real DB, the design we
landed on):

1. Whole-blob writes: two processes (the gateway/CLI writing tokens, the worker
   refreshing) can clobber each other in the small window between read and write.
   Writers reload before mutating to shrink it, but it is not atomic — replace with
   row-level writes.
2. No single-flight on refresh: concurrent readers that both find an expired token
   will each refresh, and with refresh-token rotation the loser gets invalid_grant.
   The refresh itself lives in the SDK's OAuthClientProvider (see
   activities.call_tool_activity); guarding it needs a per-(user, upstream) lock —
   in-process (oauth-local's RefreshCoordinator) and, across workers, a DB advisory
   lock or a Temporal RefreshWorkflow keyed by (user, upstream).
"""

from __future__ import annotations

import asyncio
import getpass
import json
import os
import secrets
import subprocess
import time
from pathlib import Path
from typing import Any, Protocol

from mcp.client.auth import TokenStorage
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

from . import config


class TokenVault(Protocol):
    # sessions
    async def create_session(self, user_id: str) -> str:
        """Mint an opaque session handle that resolves to user_id."""
        ...

    def user_for_session(self, session_id: str) -> str:
        """Resolve a session handle to its user id (raises KeyError if unknown)."""
        ...

    # tokens (keyed by user; the caller resolves the session first)
    def storage_for(self, user_id: str, upstream_name: str) -> TokenStorage: ...


# --- credential stores: where the JSON blob lives -------------------------


class CredentialStore(Protocol):
    def load(self) -> dict[str, Any]: ...

    def save(self, data: dict[str, Any]) -> None: ...


class FileCredentialStore(CredentialStore):
    """A 0600 JSON file (Linux/Windows). Plaintext, like Claude Code's
    ~/.claude/.credentials.json — relies on OS file permissions."""

    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text() or "{}")

    def save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = f"{self.path}.tmp"
        # Create with 0600 from the start, then atomically replace.
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        os.replace(tmp, self.path)


class KeychainCredentialStore(CredentialStore):
    """A single generic-password item in the macOS Keychain (encrypted at rest),
    holding the JSON blob — exactly how Claude Code does it on macOS."""

    def __init__(self, service: str, account: str) -> None:
        self.service = service
        self.account = account

    def load(self) -> dict[str, Any]:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", self.service,
             "-a", self.account, "-w"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            return {}  # errSecItemNotFound on first run
        return json.loads(result.stdout.strip() or "{}")

    def save(self, data: dict[str, Any]) -> None:
        # -U updates the item if it already exists. (The secret is passed as an
        # argv arg, briefly visible to `ps`; a production build would use the
        # Security framework API instead of the CLI.)
        subprocess.run(
            ["security", "add-generic-password", "-U", "-s", self.service,
             "-a", self.account, "-w", json.dumps(data)],
            check=True, capture_output=True,
        )


def open_default_vault() -> "JsonVault":
    """Pick the credential store for this platform and open the vault."""
    if config.CRED_BACKEND == "keychain":
        store: CredentialStore = KeychainCredentialStore(
            config.KEYCHAIN_SERVICE, getpass.getuser()
        )
    else:
        store = FileCredentialStore(config.CREDENTIALS_PATH)
    return JsonVault(store)


# --- the vault ------------------------------------------------------------


class JsonVault(TokenVault):
    def __init__(self, store: CredentialStore) -> None:
        self._store = store
        self._data: dict[str, Any] = store.load()
        self._data.setdefault("sessions", {})
        self._data.setdefault("tokens", {})
        self._lock = asyncio.Lock()  # serialize blob writes

    async def _mutate(self, apply) -> None:
        """Reload the blob, apply ``apply(data)``, and save — under the lock.

        Reloading before each write shrinks the window in which the gateway
        (minting sessions / writing connect tokens) and the worker (writing
        refreshed tokens) clobber each other's section of the shared blob.
        """
        async with self._lock:
            data = await asyncio.to_thread(self._store.load)
            data.setdefault("sessions", {})
            data.setdefault("tokens", {})
            apply(data)
            self._data = data
            await asyncio.to_thread(self._store.save, data)

    # --- sessions ---------------------------------------------------------

    async def create_session(self, user_id: str) -> str:
        session_id = secrets.token_urlsafe(24)
        await self._mutate(lambda d: d["sessions"].__setitem__(session_id, user_id))
        return session_id

    def user_for_session(self, session_id: str) -> str:
        user_id = self._data["sessions"].get(session_id)
        if user_id is None:
            raise KeyError(f"unknown session: {session_id!r}")
        return user_id

    # --- tokens -----------------------------------------------------------

    def _entry(self, user_id: str, upstream_name: str) -> dict[str, Any] | None:
        return self._data["tokens"].get(user_id, {}).get(upstream_name)

    def storage_for(self, user_id: str, upstream_name: str) -> "JsonTokenStorage":
        return JsonTokenStorage(self, user_id, upstream_name)


class JsonTokenStorage(TokenStorage):
    """One (user, upstream) entry as the SDK's TokenStorage protocol. Reads hit
    the in-memory document; writes mutate it and persist the whole blob."""

    def __init__(self, vault: JsonVault, user_id: str, upstream_name: str) -> None:
        self._vault = vault
        self._user_id = user_id
        self._upstream = upstream_name

    async def get_tokens(self) -> OAuthToken | None:
        entry = self._vault._entry(self._user_id, self._upstream)
        if entry is None or entry.get("token") is None:
            return None
        return OAuthToken.model_validate(entry["token"])

    def stored_expiry(self) -> float | None:
        """The absolute expiry (epoch seconds) stamped at the last set_tokens, or None.

        The SDK's OAuthClientProvider only tracks token expiry *in memory* (from a token it
        fetched/refreshed this process); it never restores it from storage on load, so a
        freshly-built provider considers any loaded token valid and skips the refresh it
        should do. We persist the absolute expiry here and re-prime the provider with it (see
        upstreams._oauth_provider) so is_token_valid() is honest across our ephemeral
        per-call/per-discovery providers. Sync (reads the in-memory blob) so provider
        construction stays non-async.
        """
        entry = self._vault._entry(self._user_id, self._upstream)
        return entry.get("expires_at") if entry else None

    async def set_tokens(self, tokens: OAuthToken) -> None:
        # Called on initial grant AND after every refresh (incl. rotation), so
        # persisting here is what stops a rotated refresh token being lost. We
        # stamp absolute expiry now, since expires_in is relative.
        def apply(d):
            entry = d["tokens"].setdefault(self._user_id, {}).setdefault(self._upstream, {})
            entry["token"] = tokens.model_dump(mode="json")
            entry["expires_at"] = (
                time.time() + tokens.expires_in if tokens.expires_in else None
            )

        await self._vault._mutate(apply)

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        entry = self._vault._entry(self._user_id, self._upstream)
        if entry is None or entry.get("client_info") is None:
            return None
        return OAuthClientInformationFull.model_validate(entry["client_info"])

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        def apply(d):
            entry = d["tokens"].setdefault(self._user_id, {}).setdefault(self._upstream, {})
            entry["client_info"] = client_info.model_dump(mode="json")

        await self._vault._mutate(apply)
