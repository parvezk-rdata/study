from __future__ import annotations

from config import Settings
from controller.auth_controller_logic import AuthControllerLogic
from controller.chat_controller_logic import ChatControllerLogic
from controller.doc_controller_logic import DocControllerLogic
from services.auth_service import AuthService
from state.auth_state import AuthState
from state.chat_state import ChatState
from state.doc_state import DocState
from ui.page import PageUI
from ui.sidebar import SidebarUI


class AppController:
    """
    Entry point for the Streamlit render cycle.
    Pure orchestration — no business logic, no state reads beyond
    what is needed to wire the render order.
    """

    def __init__(
        self,
        auth_state: AuthState,
        doc_state: DocState,
        chat_state: ChatState,
        auth_logic: AuthControllerLogic,
        doc_logic: DocControllerLogic,
        chat_logic: ChatControllerLogic,
        auth_svc: AuthService,
        page_ui: PageUI,
        sidebar_ui: SidebarUI,
        config: Settings,
    ) -> None:
        self._auth_state = auth_state
        self._doc_state = doc_state
        self._chat_state = chat_state
        self._auth_logic = auth_logic
        self._doc_logic = doc_logic
        self._chat_logic = chat_logic
        self._auth_svc = auth_svc
        self._page_ui = page_ui
        self._sidebar_ui = sidebar_ui
        self._config = config

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        self._page_ui.configure_page()
        self._page_ui.render_title()
        self._init_state()
        self._auth_logic.handle_poll()
        self._handle_sidebar()
        self._handle_session_events()
        self._doc_logic.handle_upload()
        self._chat_logic.handle_chat()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _init_state(self) -> None:
        stored_auth = self._auth_svc.load_stored_auth()
        default_mode = "ChatGPT" if stored_auth else "API key"
        self._auth_state.init(
            default_mode=default_mode,
            default_model=self._config.default_oauth_model,
        )
        self._doc_state.init()
        self._chat_state.init()

    def _handle_sidebar(self) -> None:
        stored_auth = self._auth_svc.load_stored_auth()
        event = self._sidebar_ui.render(
            stored_auth=stored_auth,
            current_mode=self._auth_state.get_mode(),
            current_model=self._auth_state.get_oauth_model(),
            login_pending=self._auth_state.is_login_pending(),
            oauth_models=self._config.oauth_models,
        )
        self._auth_logic.handle_sidebar(event)
        self._current_event = event

    def _handle_session_events(self) -> None:
        event = self._current_event
        if event.clear_conversation_clicked:
            self._chat_state.clear_history()

        if event.remove_pdf_clicked:
            self._doc_state.clear_doc()
            self._chat_state.clear_history()
