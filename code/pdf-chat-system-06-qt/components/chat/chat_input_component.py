from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget


class ChatInputComponent(QWidget):
    send_requested = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.input = QLineEdit()
        self.send_button = QPushButton("Send")

        self._build_ui()
        self.set_has_document(False)

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        layout.addWidget(self.input, 1)
        layout.addWidget(self.send_button, 0)

        self.send_button.clicked.connect(self._emit_send)
        self.input.returnPressed.connect(self._emit_send)

    def _emit_send(self) -> None:
        text = self.input.text().strip()
        if not text:
            return

        self.send_requested.emit(text)
        self.input.clear()

    def set_has_document(self, has_document: bool) -> None:
        self.input.setEnabled(has_document)
        self.send_button.setEnabled(has_document)

        if has_document:
            self.input.setPlaceholderText("Ask a question about the PDF")
        else:
            self.input.setPlaceholderText("Upload a PDF to start")