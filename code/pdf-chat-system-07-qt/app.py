from components.layout.main_window import MainWindow
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

        self.main_controller = MainController(
            window=self.window,
            store=self.store,
            llm_service=self.llm_service,
            pdf_extraction_service=self.pdf_extraction_service,
        )

    def start(self) -> None:
        self._apply_styles()
        self.main_controller.initialize()
        self.window.show()


    def _apply_styles(self) -> None:
        with open("styles/theme_slate_indigo.qss", "r") as f:
            self.window.setStyleSheet(f.read())