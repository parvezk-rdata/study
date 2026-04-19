from __future__ import annotations

from openai import OpenAI

from config import Settings
from models.chat import Message


class OpenAIClient:
    """
    Transport layer for the API key path.
    Receives ready-to-send messages from the controller and returns the reply.
    """

    def __init__(self, config: Settings) -> None:
        self._config = config

    def chat(self, messages: list[Message]) -> str:
        client = self._build_client()
        resp = client.chat.completions.create(
            model=self._config.openai_model,
            messages=[m.to_api_dict() for m in messages],
        )
        return resp.choices[0].message.content or ""

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _build_client(self) -> OpenAI:
        if not self._config.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to your .env file."
            )
        if not self._config.openai_model:
            raise RuntimeError(
                "OPENAI_MODEL is not set. Add it to your .env file "
                "(e.g. OPENAI_MODEL=gpt-4o-mini)."
            )
        return OpenAI(
            api_key=self._config.openai_api_key,
            base_url=self._config.openai_base_url,
        )
