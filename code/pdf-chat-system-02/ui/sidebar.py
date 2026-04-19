from __future__ import annotations

import streamlit as st

from models.auth import StoredAuth
from models.ui import SidebarEvent


class SidebarUI:
    """
    Renders the entire sidebar and returns a SidebarEvent.
    Completely stateless — receives all values it needs as arguments.
    """

    def render(
        self,
        stored_auth: StoredAuth | None,
        current_mode: str,
        current_model: str,
        login_pending: bool,
        oauth_models: list[str],
    ) -> SidebarEvent:
        event = SidebarEvent()

        with st.sidebar:
            event = self._render_auth_panel(
                event, stored_auth, current_mode, current_model,
                login_pending, oauth_models,
            )
            st.divider()
            event = self._render_session_panel(event)

        return event

    # ------------------------------------------------------------------
    # Auth panel
    # ------------------------------------------------------------------

    def _render_auth_panel(
        self,
        event: SidebarEvent,
        stored_auth: StoredAuth | None,
        current_mode: str,
        current_model: str,
        login_pending: bool,
        oauth_models: list[str],
    ) -> SidebarEvent:
        st.header("Auth")

        mode = st.radio(
            "Mode",
            options=["ChatGPT", "API key"],
            index=0 if current_mode == "ChatGPT" else 1,
            horizontal=True,
        )
        event.mode = mode

        if mode == "ChatGPT":
            event = self._render_chatgpt_auth(
                event, stored_auth, current_model, login_pending, oauth_models,
            )
        else:
            self._render_api_key_info(stored_auth)

        return event

    def _render_chatgpt_auth(
        self,
        event: SidebarEvent,
        stored_auth: StoredAuth | None,
        current_model: str,
        login_pending: bool,
        oauth_models: list[str],
    ) -> SidebarEvent:
        if stored_auth is None:
            if login_pending:
                st.info("Complete sign-in in your browser. Waiting for callback…")
                event.cancel_login_clicked = st.button("Cancel sign-in")
            else:
                event.sign_in_clicked = st.button("Sign in with ChatGPT")
        else:
            st.caption(f"Signed in as **{stored_auth.display_label}**")
            model = st.selectbox(
                "Model",
                options=oauth_models,
                index=oauth_models.index(current_model)
                if current_model in oauth_models
                else 0,
                help="All Codex-addressable models. Not every slug is active on every plan.",
            )
            event.model = model
            event.sign_out_clicked = st.button("Sign out")

        return event

    @staticmethod
    def _render_api_key_info(stored_auth: StoredAuth | None) -> None:
        if stored_auth is not None:
            st.caption(
                "ChatGPT tokens are still stored. "
                "They will be ignored while API key mode is active."
            )
        st.caption("Using `OPENAI_API_KEY` and `OPENAI_MODEL` from `.env`.")

    # ------------------------------------------------------------------
    # Session panel
    # ------------------------------------------------------------------

    @staticmethod
    def _render_session_panel(event: SidebarEvent) -> SidebarEvent:
        st.header("Session")
        event.clear_conversation_clicked = st.button("Clear conversation")
        event.remove_pdf_clicked = st.button("Remove PDF")
        return event
