from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, parse_qs, urlparse

import httpx

from config import Settings
from models.auth import StoredAuth


_HTML_SUCCESS = """<!doctype html>
<html><head><title>pdf-chat sign-in</title>
<style>body{font-family:system-ui,-apple-system,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#131010;color:#f1ecec}.c{text-align:center;padding:2rem}</style>
</head><body><div class="c"><h1>Signed in</h1><p>You can close this tab and return to pdf-chat.</p></div>
<script>setTimeout(()=>window.close(),1500)</script></body></html>"""


def _html_error(msg: str) -> str:
    safe = msg.replace("<", "&lt;").replace(">", "&gt;")
    return (
        "<!doctype html><html><head><title>pdf-chat sign-in failed</title></head>"
        f"<body><h1>Sign-in failed</h1><pre>{safe}</pre></body></html>"
    )


# ---------------------------------------------------------------------------
# LoginHandle
# ---------------------------------------------------------------------------

class LoginHandle:
    """Returned by AuthService.start_login(). Used to poll or cancel the flow."""

    def __init__(
        self,
        authorize_url: str,
        server: HTTPServer,
        thread: threading.Thread,
        result: dict,
    ) -> None:
        self.authorize_url = authorize_url
        self._server = server
        self._thread = thread
        self._result = result

    def poll(self) -> StoredAuth | None:
        if self._result.get("error"):
            raise RuntimeError(self._result["error"])
        stored = self._result.get("auth")
        if stored is not None:
            self._shutdown()
        return stored

    def cancel(self) -> None:
        self._result.setdefault("error", "Sign-in cancelled")
        self._shutdown()

    def _shutdown(self) -> None:
        if self._result.get("closed"):
            return
        self._result["closed"] = True
        try:
            self._server.shutdown()
            self._server.server_close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# AuthService
# ---------------------------------------------------------------------------

class AuthService:
    """Handles OAuth login, logout, token refresh, and filesystem persistence."""

    def __init__(self, config: Settings) -> None:
        self._config = config
        self._token_file = Path(config.token_file_path)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def load_stored_auth(self) -> StoredAuth | None:
        if not self._token_file.exists():
            return None
        try:
            data = json.loads(self._token_file.read_text())
            return StoredAuth.model_validate(data)
        except (json.JSONDecodeError, TypeError, ValueError):
            return None

    def save_stored_auth(self, stored: StoredAuth) -> None:
        self._token_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._token_file.with_suffix(".json.tmp")
        tmp.write_text(stored.model_dump_json(indent=2))
        os.chmod(tmp, 0o600)
        tmp.replace(self._token_file)

    def logout(self) -> None:
        self._token_file.unlink(missing_ok=True)

    # ------------------------------------------------------------------
    # Token refresh
    # ------------------------------------------------------------------

    def refresh_if_needed(self, stored: StoredAuth) -> StoredAuth:
        if stored.expires_at - 60 > time.time():
            return stored

        resp = httpx.post(
            f"{self._config.oauth_issuer}/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": stored.refresh_token,
                "client_id": self._config.oauth_client_id,
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        refreshed = self._build_stored_auth(resp.json(), fallback=stored)
        self.save_stored_auth(refreshed)
        return refreshed

    # ------------------------------------------------------------------
    # Login flow
    # ------------------------------------------------------------------

    def start_login(self) -> LoginHandle:
        verifier, challenge = self._generate_pkce_pair()
        state = self._generate_state()
        authorize_url = self._build_authorize_url(challenge, state)

        result: dict[str, Any] = {}
        handler_class = self._make_handler_class(state, verifier, result)

        server = HTTPServer(("127.0.0.1", self._config.oauth_redirect_port), handler_class)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return LoginHandle(authorize_url, server, thread, result)

    def cancel_login(self, handle: LoginHandle) -> None:
        handle.cancel()

    def poll_login(self, handle: LoginHandle) -> StoredAuth | None:
        return handle.poll()

    # ------------------------------------------------------------------
    # Private — PKCE + URL helpers
    # ------------------------------------------------------------------

    def _generate_pkce_pair(self) -> tuple[str, str]:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
        verifier = "".join(secrets.choice(alphabet) for _ in range(43))
        challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(verifier.encode("ascii")).digest()
            )
            .rstrip(b"=")
            .decode("ascii")
        )
        return verifier, challenge

    def _generate_state(self) -> str:
        return (
            base64.urlsafe_b64encode(secrets.token_bytes(32))
            .rstrip(b"=")
            .decode("ascii")
        )

    def _build_authorize_url(self, challenge: str, state: str) -> str:
        params = {
            "response_type": "code",
            "client_id": self._config.oauth_client_id,
            "redirect_uri": self._config.oauth_redirect_uri,
            "scope": "openid profile email offline_access",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "id_token_add_organizations": "true",
            "codex_cli_simplified_flow": "true",
            "state": state,
            "originator": self._config.oauth_originator,
        }
        return f"{self._config.oauth_issuer}/oauth/authorize?{urlencode(params)}"

    # ------------------------------------------------------------------
    # Private — token parsing
    # ------------------------------------------------------------------

    def _build_stored_auth(
        self, tokens: dict[str, Any], fallback: StoredAuth | None = None
    ) -> StoredAuth:
        expires_in = tokens.get("expires_in", 3600)
        return StoredAuth(
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token")
            or (fallback.refresh_token if fallback else ""),
            expires_at=time.time() + float(expires_in),
            account_id=self._account_id_from_tokens(tokens)
            or (fallback.account_id if fallback else None),
            email=self._email_from_tokens(tokens)
            or (fallback.email if fallback else None),
        )

    def _account_id_from_tokens(self, tokens: dict[str, Any]) -> str | None:
        for key in ("id_token", "access_token"):
            tok = tokens.get(key)
            if not tok:
                continue
            claims = self._parse_jwt_claims(tok)
            if not claims:
                continue
            account_id = claims.get("chatgpt_account_id")
            if account_id:
                return account_id
            nested = claims.get("https://api.openai.com/auth") or {}
            if isinstance(nested, dict) and nested.get("chatgpt_account_id"):
                return nested["chatgpt_account_id"]
            orgs = claims.get("organizations") or []
            if isinstance(orgs, list) and orgs and isinstance(orgs[0], dict):
                org_id = orgs[0].get("id")
                if org_id:
                    return org_id
        return None

    def _email_from_tokens(self, tokens: dict[str, Any]) -> str | None:
        tok = tokens.get("id_token") or tokens.get("access_token")
        if not tok:
            return None
        claims = self._parse_jwt_claims(tok) or {}
        return claims.get("email")

    @staticmethod
    def _parse_jwt_claims(token: str) -> dict[str, Any] | None:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        try:
            padded = parts[1] + "=" * (-len(parts[1]) % 4)
            return json.loads(base64.urlsafe_b64decode(padded))
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Private — OAuth callback handler
    # ------------------------------------------------------------------

    def _make_handler_class(self, state: str, verifier: str, result: dict):
        config = self._config
        build_stored_auth = self._build_stored_auth
        save = self.save_stored_auth

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args, **kwargs) -> None:
                pass

            def do_GET(self) -> None:
                if not self.path.startswith("/auth/callback"):
                    self.send_response(404)
                    self.end_headers()
                    return

                query = parse_qs(urlparse(self.path).query)
                err = query.get("error", [None])[0]
                if err:
                    desc = query.get("error_description", [err])[0]
                    result["error"] = desc
                    self._respond(200, _html_error(desc))
                    return

                code = query.get("code", [None])[0]
                recv_state = query.get("state", [None])[0]
                if not code:
                    result["error"] = "Missing authorization code"
                    self._respond(400, _html_error(result["error"]))
                    return
                if recv_state != state:
                    result["error"] = "Invalid state (possible CSRF)"
                    self._respond(400, _html_error(result["error"]))
                    return

                try:
                    resp = httpx.post(
                        f"{config.oauth_issuer}/oauth/token",
                        data={
                            "grant_type": "authorization_code",
                            "code": code,
                            "redirect_uri": config.oauth_redirect_uri,
                            "client_id": config.oauth_client_id,
                            "code_verifier": verifier,
                        },
                        timeout=30.0,
                    )
                    resp.raise_for_status()
                    stored = build_stored_auth(resp.json())
                    save(stored)
                    result["auth"] = stored
                    self._respond(200, _HTML_SUCCESS)
                except Exception as e:
                    result["error"] = f"Token exchange failed: {e}"
                    self._respond(500, _html_error(result["error"]))

            def _respond(self, code: int, body: str) -> None:
                self.send_response(code)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))

        return Handler
