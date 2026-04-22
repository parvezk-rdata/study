from PyQt6.QtWidgets import QFileDialog

from components.layout.main_window import MainWindow
from controllers.chat_controller import ChatController
from controllers.document_controller import DocumentController
from models.document_models import DocumentInfo
from state.app_state_store import AppStateStore


class MainController:
    def __init__(
        self,
        window: MainWindow,
        store: AppStateStore,
        document_controller: DocumentController,
        chat_controller: ChatController,
    ) -> None:
        self.window = window
        self.store = store
        self.document_controller = document_controller
        self.chat_controller = chat_controller

    def initialize(self) -> None:
        self._connect_ui_events()
        self._connect_store_events()
        self._configure_static_ui()
        self._render_initial_state()

    def _connect_ui_events(self) -> None:
        panel = self.window.get_pdf_panel_component()
        chat_input = self.window.get_chat_input_component()

        panel.upload_requested.connect(self.handle_upload_pdf)
        panel.clear_chat_requested.connect(self.handle_clear_chat)
        panel.remove_pdf_requested.connect(self.handle_remove_pdf)
        chat_input.send_requested.connect(self.handle_send_message)

    def _connect_store_events(self) -> None:
        self.store.document_changed.connect(self.on_document_changed)
        self.store.chat_changed.connect(self.on_chat_changed)
        self.store.status_changed.connect(self.on_status_changed)

    def _configure_static_ui(self) -> None:
        panel = self.window.get_pdf_panel_component()
        chat_input = self.window.get_chat_input_component()

        panel.set_title_text("PDF")
        panel.set_upload_button_text("Upload PDF")
        panel.set_clear_chat_button_text("Clear conversation")
        panel.set_remove_pdf_button_text("Remove PDF")

        chat_input.set_send_button_text("Send")

        panel.get_title_label().setStyleSheet("font-weight: bold; font-size: 14px;")
        self.window.statusBar().showMessage("Ready")

    def _render_initial_state(self) -> None:
        state = self.store.get_state()
        self._render_document_section(state.document)
        self._render_chat_input_section(state.document is not None)
        self.on_chat_changed(state.chat_history)
        self.on_status_changed(state.status_message or "Ready")

    def handle_upload_pdf(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Select PDF",
            "",
            "PDF Files (*.pdf)",
        )
        if not file_path:
            return

        self.document_controller.load_pdf(file_path)

    def handle_send_message(self, text: str) -> None:
        self.chat_controller.send_message(text)

    def handle_clear_chat(self) -> None:
        self.store.clear_chat()
        self.store.set_status("Conversation cleared.")

    def handle_remove_pdf(self) -> None:
        self.document_controller.remove_pdf()

    def on_document_changed(self, document: DocumentInfo | None) -> None:
        self._render_document_section(document)
        self._render_chat_input_section(document is not None)

    def on_chat_changed(self, history: list) -> None:
        items: list[dict[str, str]] = []

        for message in history:
            header_text = self._format_message_header(message.role)
            content_text = message.content
            items.append({"header": header_text, "content": content_text})

        self.window.get_chat_history_component().set_message_items(items)

    def on_status_changed(self, message: str) -> None:
        self.window.statusBar().showMessage(message)

    def _render_document_section(self, document: DocumentInfo | None) -> None:
        panel = self.window.get_pdf_panel_component()

        if document is None:
            panel.set_file_text("No PDF selected")
            panel.set_info_text("Upload a PDF to start chatting.")

            panel.get_clear_chat_button().setEnabled(False)
            panel.get_remove_pdf_button().setEnabled(False)

            panel.get_file_label().setVisible(True)
            panel.get_info_label().setVisible(True)
            return

        panel.set_file_text(document.filename)
        panel.set_info_text(self._build_document_info_text(document))

        panel.get_clear_chat_button().setEnabled(True)
        panel.get_remove_pdf_button().setEnabled(True)

        panel.get_file_label().setVisible(True)
        panel.get_info_label().setVisible(True)

    def _render_chat_input_section(self, has_document: bool) -> None:
        chat_input = self.window.get_chat_input_component()

        if has_document:
            chat_input.set_placeholder_text("Ask a question about the PDF")
            chat_input.get_input().setEnabled(True)
            chat_input.get_send_button().setEnabled(True)
        else:
            chat_input.set_placeholder_text("Upload a PDF to start")
            chat_input.get_input().setEnabled(False)
            chat_input.get_send_button().setEnabled(False)

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