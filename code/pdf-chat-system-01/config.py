from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Single source of truth for all configuration.
    Values are loaded from environment variables and .env file automatically.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # OpenAI API key path
    # ------------------------------------------------------------------
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="", alias="OPENAI_MODEL")
    openai_base_url: str | None = Field(default=None, alias="OPENAI_BASE_URL")

    # ------------------------------------------------------------------
    # OAuth / Codex path
    # ------------------------------------------------------------------
    oauth_client_id: str = "app_EMoamEEZ73f0CkXaXp7hrann"
    oauth_issuer: str = "https://auth.openai.com"
    oauth_redirect_port: int = 1455
    oauth_originator: str = "pdf-chat"
    codex_api_endpoint: str = "https://chatgpt.com/backend-api/codex/responses"

    oauth_models: list[str] = [
        "gpt-5.3-codex",
        "gpt-5.4",
        "gpt-5.2-codex",
        "gpt-5.1-codex-max",
        "gpt-5.2",
        "gpt-5.1-codex-mini",
        "gpt-5.1-codex",
        "gpt-5.1",
        "gpt-5-codex",
        "gpt-5-codex-mini",
        "gpt-5",
        "gpt-oss-120b",
        "gpt-oss-20b",
    ]
    default_oauth_model: str = "gpt-5.3-codex"

    # ------------------------------------------------------------------
    # Token / context budget
    # ------------------------------------------------------------------
    context_token_budget: int = 100_000
    chars_per_token: int = 4

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------
    token_file_path: str = ".pdf-chat/auth.json"
    login_timeout_seconds: int = 180

    # ------------------------------------------------------------------
    # Derived helpers
    # ------------------------------------------------------------------
    @property
    def oauth_redirect_uri(self) -> str:
        return f"http://localhost:{self.oauth_redirect_port}/auth/callback"

    @property
    def max_pdf_chars(self) -> int:
        return self.context_token_budget * self.chars_per_token
