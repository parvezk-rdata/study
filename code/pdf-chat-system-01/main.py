from __future__ import annotations

from config import Settings
from controller.app_controller import AppController
from controller.auth_controller_logic import AuthControllerLogic
from controller.chat_controller_logic import ChatControllerLogic
from controller.doc_controller_logic import DocControllerLogic
from services.auth_service import AuthService
from services.pdf_service import PDFService
from state.auth_state import AuthState
from state.chat_state import ChatState
from state.doc_state import DocState
from ui.chat_panel import ChatPanelUI
from ui.page import PageUI
from ui.pdf_panel import PDFPanelUI
from ui.sidebar import SidebarUI


def main() -> None:
    config = Settings()

    # State
    auth_state = AuthState()
    doc_state = DocState()
    chat_state = ChatState()

    # Services
    auth_svc = AuthService(config)
    pdf_svc = PDFService()

    # UI
    page_ui = PageUI()
    sidebar_ui = SidebarUI()
    pdf_ui = PDFPanelUI()
    chat_ui = ChatPanelUI()

    # Controller logic
    auth_logic = AuthControllerLogic(auth_state, auth_svc, sidebar_ui, config)
    doc_logic = DocControllerLogic(doc_state, chat_state, pdf_svc, pdf_ui, config)
    chat_logic = ChatControllerLogic(auth_state, doc_state, chat_state, chat_ui, auth_svc, config)

    # Orchestrator
    controller = AppController(
        auth_state=auth_state,
        doc_state=doc_state,
        chat_state=chat_state,
        auth_logic=auth_logic,
        doc_logic=doc_logic,
        chat_logic=chat_logic,
        auth_svc=auth_svc,
        page_ui=page_ui,
        sidebar_ui=sidebar_ui,
        config=config,
    )
    controller.run()


if __name__ == "__main__":
    main()
