from controllers.chat_controller import ChatController
from controllers.document_controller import DocumentController
from controllers.main_controller import MainController
from components.layout.main_window import MainWindow
from services.llm_service import LLMService
from services.pdf_extraction_service import PDFExtractionService
from state.app_state_store import AppStateStore


class PDFChatApplication:
    def __init__(self) -> None:
        self.store = AppStateStore()
        self.pdf_service = PDFExtractionService()
        self.llm_service = LLMService()

        self.window = MainWindow()

        self.document_controller = DocumentController(
            store=self.store,
            pdf_service=self.pdf_service,
            llm_service=self.llm_service,
        )
        self.chat_controller = ChatController(
            store=self.store,
            llm_service=self.llm_service,
        )
        self.main_controller = MainController(
            window=self.window,
            store=self.store,
            document_controller=self.document_controller,
            chat_controller=self.chat_controller,
        )

    def start(self) -> None:
        self.main_controller.initialize()
        self.window.show()
    
    def start(self) -> None:
        self._apply_styles()
        self.main_controller.initialize()
        self.window.show()


    def _apply_styles(self) -> None:
        with open("styles/theme_slate_indigo.qss", "r") as f:
            self.window.setStyleSheet(f.read())