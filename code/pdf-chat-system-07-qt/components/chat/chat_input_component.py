from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget


class ChatInputComponent(QWidget):
    send_requested = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    def _create_widgets(self) -> None:
        self._input = QLineEdit()
        self._send_button = QPushButton()

    def _build_layout(self) -> None:
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(8)

        self._layout.addWidget(self._input, 1)
        self._layout.addWidget(self._send_button, 0)

    def _connect_signals(self) -> None:
        self._send_button.clicked.connect(self._emit_send)
        self._input.returnPressed.connect(self._emit_send)

    def _emit_send(self) -> None:
        self.send_requested.emit(self._input.text())

    def get_input(self) -> QLineEdit:
        return self._input

    def get_send_button(self) -> QPushButton:
        return self._send_button

    def get_input_text(self) -> str:
        return self._input.text()

    def set_input_text(self, text: str) -> None:
        self._input.setText(text)

    def clear_input(self) -> None:
        self._input.clear()

    def set_placeholder_text(self, text: str) -> None:
        self._input.setPlaceholderText(text)

    def set_send_button_text(self, text: str) -> None:
        self._send_button.setText(text)