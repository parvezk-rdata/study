from components.layout.main_window import MainWindow
from components.system.file_dialog_component import FileDialogComponent
from controllers.component_controllers.chat_history_controller import (
    ChatHistoryController,
)
from controllers.component_controllers.chat_input_controller import ChatInputController
from controllers.component_controllers.file_dialog_controller import (
    FileDialogController,
)
from controllers.component_controllers.pdf_panel_controller import PDFPanelController
from controllers.domain_controllers.llm_controller import LLMController
from controllers.domain_controllers.pdf_controller import PDFController
from models.chat_models import ChatMessage
from models.document_models import DocumentInfo
from services.llm_service import LLMService
from services.pdf_extraction_service import PDFExtractionService
from state.app_state_store import AppStateStore


class MainController:
    def __init__( self, window: MainWindow ) -> None:
        self.window = window
        self.store = AppStateStore()

        llm_service = LLMService();

        self.pdf_controller = PDFController(
            pdf_service=PDFExtractionService(),
            llm_service=llm_service,
        )
        self.llm_controller = LLMController(
            llm_service=llm_service,
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

        self.file_dialog_component = FileDialogComponent()
        self.file_dialog_controller = FileDialogController(
            component=self.file_dialog_component
        )

    def initialize(self) -> None:
        self._connect_component_events()
        self._connect_store_events()
        self._initialize_static_ui()
        self._render_from_state()

    def _connect_component_events(self) -> None:
        pdf_panel = self.window.get_pdf_panel_component()
        chat_input = self.window.get_chat_input_component()

        pdf_panel.upload_requested.connect(self.handle_upload_pdf_requested)
        pdf_panel.clear_chat_requested.connect(self.handle_clear_chat_requested)
        pdf_panel.remove_pdf_requested.connect(self.handle_remove_pdf_requested)
        chat_input.send_requested.connect(self.handle_send_message_requested)

        self.file_dialog_component.file_selected.connect(
            self.handle_pdf_file_selected
        )

    def _connect_store_events(self) -> None:
        self.store.document_changed.connect(self.handle_document_changed)
        self.store.chat_changed.connect(self.handle_chat_changed)
        self.store.status_changed.connect(self.handle_status_changed)

    def _initialize_static_ui(self) -> None:
        self.pdf_panel_controller.initialize_component(
            title_text="PDF",
            upload_button_text="Upload PDF",
            clear_chat_button_text="Clear conversation",
            remove_pdf_button_text="Remove PDF",
            title_style="font-weight: bold; font-size: 14px;",
        )

        self.chat_input_controller.initialize_component(
            send_button_text="Send",
        )

        self.window.statusBar().showMessage("Ready")

    def _render_from_state(self) -> None:
        state = self.store.get_state()

        self._render_document_section(state.document)
        self._render_chat_history_section(state.chat_history)
        self._render_status_section(state.status_message or "Ready")

    def handle_upload_pdf_requested(self) -> None:
        self.file_dialog_controller.handle_open_pdf_dialog(self.window)

    def handle_pdf_file_selected(self, file_path: str) -> None:
        current_document = self.store.get_state().document
        self.store.set_status("Extracting text from PDF...")

        result = self.pdf_controller.load_pdf(
            file_path=file_path,
            current_document=current_document,
        )

        if result.success and result.document is not None:
            self.store.set_document(result.document)
            if result.reset_chat:
                self.store.clear_chat()

        self.store.set_status(result.status_message)

    def handle_clear_chat_requested(self) -> None:
        self.store.clear_chat()
        self.store.set_status("Conversation cleared.")
        self.chat_input_controller.handle_chat_cleared()

        current_document = self.store.get_state().document
        if current_document is not None:
            self.pdf_panel_controller.handle_chat_cleared(
                file_text=current_document.filename,
                info_text=self._build_document_info_text(current_document),
            )

    def handle_remove_pdf_requested(self) -> None:
        self.store.clear_document()
        self.store.clear_chat()
        self.store.set_status(self.pdf_controller.remove_pdf())

        self.pdf_panel_controller.handle_pdf_removed(
            file_text="No PDF selected",
            info_text="Upload a PDF to start chatting.",
        )
        self.chat_input_controller.handle_pdf_removed(
            placeholder_text="Upload a PDF to start",
        )

    def handle_send_message_requested(self, text: str) -> None:
        state = self.store.get_state()

        result = self.llm_controller.send_message(
            user_text=text,
            current_document=state.document,
            chat_history=state.chat_history,
        )

        if result.success and result.user_message is not None:
            self.store.add_chat_message(
                ChatMessage(role="user", content=result.user_message)
            )

        if result.success and result.assistant_message is not None:
            self.store.add_chat_message(
                ChatMessage(role="assistant", content=result.assistant_message)
            )
            self.chat_input_controller.handle_message_sent()

        self.store.set_status(result.status_message)

    def handle_document_changed(self, document: DocumentInfo | None) -> None:
        self._render_document_section(document)

    def handle_chat_changed(self, history: list[ChatMessage]) -> None:
        self._render_chat_history_section(history)

    def handle_status_changed(self, message: str) -> None:
        self._render_status_section(message)

    def _render_document_section(self, document: DocumentInfo | None) -> None:
        if document is None:
            self.pdf_panel_controller.handle_no_pdf_state(
                file_text="No PDF selected",
                info_text="Upload a PDF to start chatting.",
            )
            self.chat_input_controller.handle_no_pdf_state(
                placeholder_text="Upload a PDF to start",
            )
            return

        self.pdf_panel_controller.handle_pdf_loaded(
            file_text=document.filename,
            info_text=self._build_document_info_text(document),
        )
        self.chat_input_controller.handle_pdf_loaded(
            placeholder_text="Ask a question about the PDF",
        )

    def _render_chat_history_section(self, history: list[ChatMessage]) -> None:
        items: list[dict[str, str]] = []

        for message in history:
            items.append(
                {
                    "header": self._format_message_header(message.role),
                    "content": message.content,
                }
            )

        self.chat_history_controller.render_messages(items)

    def _render_status_section(self, message: str) -> None:
        self.window.statusBar().showMessage(message)

    def _build_document_info_text(self, document: DocumentInfo) -> str:
        lines = [
            f"Pages: {document.page_count}",
            f"Method: {document.extraction_method}",
            f"Characters: {document.char_count:,}",
        ]

        if document.truncated:
            lines.append("")
            lines.append(
                "Warning: PDF exceeds the context budget. Later pages will be truncated during chat."
            )

        return "\n".join(lines)

    def _format_message_header(self, role: str) -> str:
        if role == "user":
            return "You"
        if role == "assistant":
            return "Assistant"
        return role.capitalize()