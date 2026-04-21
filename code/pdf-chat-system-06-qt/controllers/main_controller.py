from PyQt6.QtWidgets import QFileDialog

from controllers.chat_controller import ChatController
from controllers.document_controller import DocumentController
from models.document_models import DocumentInfo
from state.app_state_store import AppStateStore
from components.layout.main_window import MainWindow


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
        self._render_initial_state()

    def _connect_ui_events(self) -> None:
        self.window.pdf_panel_component.upload_requested.connect(self.handle_upload_pdf)
        self.window.chat_input_component.send_requested.connect(self.handle_send_message)
        self.window.clear_chat_button.clicked.connect(self.handle_clear_chat)
        self.window.remove_pdf_button.clicked.connect(self.handle_remove_pdf)

    def _connect_store_events(self) -> None:
        self.store.document_changed.connect(self.on_document_changed)
        self.store.chat_changed.connect(self.on_chat_changed)
        self.store.status_changed.connect(self.on_status_changed)

    def _render_initial_state(self) -> None:
        state = self.store.get_state()
        self.on_document_changed(state.document)
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
        self.window.pdf_panel_component.set_document(document)
        self.window.chat_input_component.set_has_document(document is not None)

    def on_chat_changed(self, history: list) -> None:
        self.window.chat_history_component.set_messages(history)

    def on_status_changed(self, message: str) -> None:
        self.window.statusBar().showMessage(message)