from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    """A single message in the conversation history."""
    role: Literal["user", "assistant"]
    content: str

    def to_api_dict(self) -> dict:
        """Convert to the format expected by the OpenAI SDK."""
        return {"role": self.role, "content": self.content}

    def to_responses_item(self) -> dict:
        """Convert to the input-item format expected by the OAuth / Codex API."""
        content_type = "output_text" if self.role == "assistant" else "input_text"
        return {
            "role": self.role,
            "content": [{"type": content_type, "text": self.content}],
        }
