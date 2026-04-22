from components.layout.main_window import MainWindow
from controllers.component_controllers.chat_history_controller import (
    ChatHistoryController,
)
from controllers.component_controllers.chat_input_controller import ChatInputController
from controllers.component_controllers.pdf_panel_controller import PDFPanelController
from controllers.domain_controllers.llm_controller import LLMController
from controllers.domain_controllers.pdf_controller import PDFController
from controllers.main_controller import MainController
from services.llm_service import LLMService
from services.pdf_extraction_service import PDFExtractionService
from state.app_state_store import AppStateStore


class PDFChatApplication:
    def __init__(self) -> None:
        self.store = AppStateStore()

        self.llm_service = LLMService()
        self.pdf_extraction_service = PDFExtractionService()

        self.window = MainWindow()

        self.llm_controller = LLMController(llm_service=self.llm_service)
        self.pdf_controller = PDFController(
            pdf_service=self.pdf_extraction_service,
            llm_service=self.llm_service,
        )

        self.pdf_panel_controller = PDFPanelController(
            component=self.window.get_pdf_panel_component()
        )
        self.chat_history_controller = ChatHistoryController(
            component=self.window.get_chat_history_component()
        )
        self.chat_input_controller = ChatInputController(
            component=self.window.get_chat_input_component()
        )

        self.main_controller = MainController(
            window=self.window,
            store=self.store,
            pdf_controller=self.pdf_controller,
            llm_controller=self.llm_controller,
            pdf_panel_controller=self.pdf_panel_controller,
            chat_history_controller=self.chat_history_controller,
            chat_input_controller=self.chat_input_controller,
        )

    def start(self) -> None:
        self._apply_styles()
        self.main_controller.initialize()
        self.window.show()


    def _apply_styles(self) -> None:
        with open("styles/theme_slate_indigo.qss", "r") as f:
            self.window.setStyleSheet(f.read())