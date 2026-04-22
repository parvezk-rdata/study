from PyQt6.QtWidgets import QFileDialog

from components.layout.main_window import MainWindow
from controllers.component_controllers.chat_history_controller import (
    ChatHistoryController,
)
from controllers.component_controllers.chat_input_controller import ChatInputController
from controllers.component_controllers.pdf_panel_controller import PDFPanelController
from controllers.domain_controllers.llm_controller import LLMController
from controllers.domain_controllers.pdf_controller import PDFController
from models.chat_models import ChatMessage
from models.document_models import DocumentInfo
from state.app_state_store import AppStateStore


class MainController:
    def __init__(
        self,
        window: MainWindow,
        store: AppStateStore,
        pdf_controller: PDFController,
        llm_controller: LLMController,
        pdf_panel_controller: PDFPanelController,
        chat_history_controller: ChatHistoryController,
        chat_input_controller: ChatInputController,
    ) -> None:
        self.window = window
        self.store = store
        self.pdf_controller = pdf_controller
        self.llm_controller = llm_controller
        self.pdf_panel_controller = pdf_panel_controller
        self.chat_history_controller = chat_history_controller
        self.chat_input_controller = chat_input_controller

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

    def _connect_store_events(self) -> None:
        self.store.document_changed.connect(self.handle_document_changed)
        self.store.chat_changed.connect(self.handle_chat_changed)
        self.store.status_changed.connect(self.handle_status_changed)

    def _initialize_static_ui(self) -> None:
        self.pdf_panel_controller.set_static_texts(
            title_text="PDF",
            upload_button_text="Upload PDF",
            clear_chat_button_text="Clear conversation",
            remove_pdf_button_text="Remove PDF",
        )
        self.pdf_panel_controller.apply_title_style(
            "font-weight: bold; font-size: 14px;"
        )

        self.chat_input_controller.set_static_texts(
            send_button_text="Send",
        )

        self.window.statusBar().showMessage("Ready")

    def _render_from_state(self) -> None:
        state = self.store.get_state()

        self._render_document_section(state.document)
        self._render_chat_history_section(state.chat_history)
        self._render_status_section(state.status_message or "Ready")

    def handle_upload_pdf_requested(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Select PDF",
            "",
            "PDF Files (*.pdf)",
        )
        if not file_path:
            return

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

    def handle_remove_pdf_requested(self) -> None:
        self.store.clear_document()
        self.store.clear_chat()
        self.store.set_status(self.pdf_controller.remove_pdf())

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
            self.chat_input_controller.clear_input()

        self.store.set_status(result.status_message)

    def handle_document_changed(self, document: DocumentInfo | None) -> None:
        self._render_document_section(document)

    def handle_chat_changed(self, history: list[ChatMessage]) -> None:
        self._render_chat_history_section(history)

    def handle_status_changed(self, message: str) -> None:
        self._render_status_section(message)

    def _render_document_section(self, document: DocumentInfo | None) -> None:
        if document is None:
            self.pdf_panel_controller.render_file_text("No PDF selected")
            self.pdf_panel_controller.render_info_text(
                "Upload a PDF to start chatting."
            )
            self.pdf_panel_controller.set_clear_chat_enabled(False)
            self.pdf_panel_controller.set_remove_pdf_enabled(False)
            self.pdf_panel_controller.set_file_visible(True)
            self.pdf_panel_controller.set_info_visible(True)

            self.chat_input_controller.set_placeholder_text("Upload a PDF to start")
            self.chat_input_controller.set_input_enabled(False)
            self.chat_input_controller.set_send_enabled(False)
            return

        self.pdf_panel_controller.render_file_text(document.filename)
        self.pdf_panel_controller.render_info_text(
            self._build_document_info_text(document)
        )
        self.pdf_panel_controller.set_clear_chat_enabled(True)
        self.pdf_panel_controller.set_remove_pdf_enabled(True)
        self.pdf_panel_controller.set_file_visible(True)
        self.pdf_panel_controller.set_info_visible(True)

        self.chat_input_controller.set_placeholder_text(
            "Ask a question about the PDF"
        )
        self.chat_input_controller.set_input_enabled(True)
        self.chat_input_controller.set_send_enabled(True)

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