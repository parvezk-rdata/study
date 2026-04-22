from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class PDFPanelComponent(QWidget):
    upload_requested = pyqtSignal()
    clear_chat_requested = pyqtSignal()
    remove_pdf_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    def _create_widgets(self) -> None:
        self._title_label = QLabel()
        self._file_label = QLabel()
        self._info_label = QLabel()

        self._upload_button = QPushButton()
        self._clear_chat_button = QPushButton()
        self._remove_pdf_button = QPushButton()

        self._title_label.setWordWrap(True)
        self._file_label.setWordWrap(True)
        self._info_label.setWordWrap(True)

    def _build_layout(self) -> None:
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(8)

        self._layout.addWidget(self._title_label)
        self._layout.addWidget(self._file_label)
        self._layout.addWidget(self._upload_button)
        self._layout.addWidget(self._clear_chat_button)
        self._layout.addWidget(self._remove_pdf_button)
        self._layout.addWidget(self._info_label)
        self._layout.addStretch(1)

    def _connect_signals(self) -> None:
        self._upload_button.clicked.connect(self.upload_requested.emit)
        self._clear_chat_button.clicked.connect(self.clear_chat_requested.emit)
        self._remove_pdf_button.clicked.connect(self.remove_pdf_requested.emit)

    def get_title_label(self) -> QLabel:
        return self._title_label

    def get_file_label(self) -> QLabel:
        return self._file_label

    def get_info_label(self) -> QLabel:
        return self._info_label

    def get_upload_button(self) -> QPushButton:
        return self._upload_button

    def get_clear_chat_button(self) -> QPushButton:
        return self._clear_chat_button

    def get_remove_pdf_button(self) -> QPushButton:
        return self._remove_pdf_button

    def set_title_text(self, text: str) -> None:
        self._title_label.setText(text)

    def set_file_text(self, text: str) -> None:
        self._file_label.setText(text)

    def set_info_text(self, text: str) -> None:
        self._info_label.setText(text)

    def set_upload_button_text(self, text: str) -> None:
        self._upload_button.setText(text)

    def set_clear_chat_button_text(self, text: str) -> None:
        self._clear_chat_button.setText(text)

    def set_remove_pdf_button_text(self, text: str) -> None:
        self._remove_pdf_button.setText(text)