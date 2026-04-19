from __future__ import annotations

import json
import platform
import uuid

import httpx

from config import Settings
from models.auth import StoredAuth


class OAuthClient:
    """
    Transport layer for the OAuth path.
    Receives ready-to-send instructions and input items from the controller
    and returns the reply via SSE streaming.
    """

    def __init__(self, config: Settings, stored_auth: StoredAuth) -> None:
        self._config = config
        self._stored_auth = stored_auth

    def chat(self, instructions: str, input_items: list[dict]) -> str:
        headers = self._build_headers()
        body = self._build_body(instructions, input_items)
        return self._execute_stream(headers, body)

    # ------------------------------------------------------------------
    # Private — request construction
    # ------------------------------------------------------------------

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self._stored_auth.access_token}",
            "originator": self._config.oauth_originator,
            "User-Agent": f"pdf-chat/0.1 ({platform.system().lower()})",
            "session_id": str(uuid.uuid4()),
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        if self._stored_auth.account_id:
            headers["ChatGPT-Account-Id"] = self._stored_auth.account_id
        return headers

    def _build_body(self, instructions: str, input_items: list[dict]) -> dict:
        return {
            "model": self._config.default_oauth_model,
            "instructions": instructions,
            "input": input_items,
            "tools": [],
            "tool_choice": "auto",
            "parallel_tool_calls": True,
            "store": False,
            "stream": True,
            "include": [],
            "prompt_cache_key": str(uuid.uuid4()),
        }

    # ------------------------------------------------------------------
    # Private — SSE streaming
    # ------------------------------------------------------------------

    def _execute_stream(self, headers: dict, body: dict) -> str:
        chunks: list[str] = []
        with httpx.stream(
            "POST",
            self._config.codex_api_endpoint,
            headers=headers,
            json=body,
            timeout=120.0,
        ) as resp:
            if resp.status_code >= 400:
                raise RuntimeError(
                    f"Codex API error {resp.status_code}: "
                    f"{resp.read().decode('utf-8', 'replace')[:500]}"
                )
            for line in resp.iter_lines():
                chunk = self._parse_sse_line(line, chunks)
                if chunk:
                    chunks.append(chunk)

        return "".join(chunks)

    @staticmethod
    def _parse_sse_line(line: str, accumulated: list[str]) -> str | None:
        if not line or not line.startswith("data:"):
            return None

        payload = line[5:].strip()
        if payload == "[DONE]" or not payload:
            return None

        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            return None

        etype = event.get("type", "")

        if etype == "response.output_text.delta":
            delta = event.get("delta")
            return delta if isinstance(delta, str) else None

        if etype == "response.completed" and not accumulated:
            for item in event.get("response", {}).get("output", []) or []:
                for c in item.get("content", []) or []:
                    if c.get("type") in ("output_text", "text"):
                        return c.get("text", "") or None

        return None
