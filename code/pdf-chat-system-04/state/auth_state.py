from __future__ import annotations

import streamlit as st

from models.auth import StoredAuth


class AuthState:
    """Manages all auth-related entries in st.session_state."""

    def init(self, default_mode: str, default_model: str) -> None:
        st.session_state.setdefault("auth_mode", default_mode)
        st.session_state.setdefault("oauth_model", default_model)
        st.session_state.setdefault("login_handle", None)
        st.session_state.setdefault("login_started_at", None)

    # ------------------------------------------------------------------
    # Auth mode
    # ------------------------------------------------------------------

    def get_mode(self) -> str:
        return st.session_state.get("auth_mode", "API key")

    def set_mode(self, mode: str) -> None:
        st.session_state["auth_mode"] = mode

    # ------------------------------------------------------------------
    # OAuth model
    # ------------------------------------------------------------------

    def get_oauth_model(self) -> str:
        return st.session_state.get("oauth_model", "")

    def set_oauth_model(self, model: str) -> None:
        st.session_state["oauth_model"] = model

    # ------------------------------------------------------------------
    # Login handle + timestamp
    # ------------------------------------------------------------------

    def get_login_handle(self):
        return st.session_state.get("login_handle")

    def begin_login(self, handle, started_at: float) -> None:
        st.session_state["login_handle"] = handle
        st.session_state["login_started_at"] = started_at

    def clear_login(self) -> None:
        st.session_state["login_handle"] = None
        st.session_state["login_started_at"] = None

    def get_login_started_at(self) -> float | None:
        return st.session_state.get("login_started_at")

    # ------------------------------------------------------------------
    # Derived helpers
    # ------------------------------------------------------------------

    def is_login_pending(self) -> bool:
        return self.get_login_handle() is not None

    def is_oauth_mode(self) -> bool:
        return self.get_mode() == "ChatGPT"
