from __future__ import annotations

import time
import webbrowser

import streamlit as st

from config import Settings
from models.ui import SidebarEvent
from services.auth_service import AuthService
from state.auth_state import AuthState
from ui.sidebar import SidebarUI


class AuthControllerLogic:
    """
    Handles all auth-related control flow:
    OAuth polling, login, logout, and sidebar auth events.
    Reads and writes AuthState only.
    """

    def __init__(
        self,
        auth_state: AuthState,
        auth_svc: AuthService,
        sidebar_ui: SidebarUI,
        config: Settings,
    ) -> None:
        self._auth_state = auth_state
        self._auth_svc = auth_svc
        self._sidebar_ui = sidebar_ui
        self._config = config

    # ------------------------------------------------------------------
    # OAuth polling
    # ------------------------------------------------------------------

    def handle_poll(self) -> None:
        handle = self._auth_state.get_login_handle()
        if handle is None:
            return

        try:
            stored = self._auth_svc.poll_login(handle)
        except RuntimeError as e:
            self._auth_state.clear_login()
            st.error(f"Sign-in failed: {e}")
            return

        if stored is not None:
            self._auth_state.clear_login()
            st.success("Signed in with ChatGPT.")
            st.rerun()
            return

        started = self._auth_state.get_login_started_at() or time.time()
        if time.time() - started > self._config.login_timeout_seconds:
            self._auth_svc.cancel_login(handle)
            self._auth_state.clear_login()
            st.error("Sign-in timed out. Try again.")
            return

        time.sleep(1.0)
        st.rerun()

    # ------------------------------------------------------------------
    # Sidebar auth events
    # ------------------------------------------------------------------

    def handle_sidebar(self, event: SidebarEvent) -> None:
        self._auth_state.set_mode(event.mode)
        if event.model:
            self._auth_state.set_oauth_model(event.model)

        if event.sign_in_clicked:
            self._start_login()

        if event.cancel_login_clicked:
            handle = self._auth_state.get_login_handle()
            if handle:
                self._auth_svc.cancel_login(handle)
            self._auth_state.clear_login()
            st.rerun()

        if event.sign_out_clicked:
            self._auth_svc.logout()
            st.rerun()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _start_login(self) -> None:
        try:
            handle = self._auth_svc.start_login()
        except OSError as e:
            st.error(
                f"Could not start local callback server on port "
                f"{self._config.oauth_redirect_port}: {e}"
            )
            return
        self._auth_state.begin_login(handle, time.time())
        webbrowser.open(handle.authorize_url)
        st.rerun()
