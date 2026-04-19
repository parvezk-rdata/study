from __future__ import annotations

from pydantic import BaseModel


class StoredAuth(BaseModel):
    """
    Persisted OAuth credentials.
    Loaded from / saved to disk by AuthService.
    """
    access_token: str
    refresh_token: str
    expires_at: float
    account_id: str | None = None
    email: str | None = None

    @property
    def display_label(self) -> str:
        """Human-readable label for the signed-in account."""
        return self.email or self.account_id or "ChatGPT account"
