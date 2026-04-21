from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class PDFUploadComponent(QWidget):
    upload_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.title_label = QLabel("PDF")
        self.file_label = QLabel("No PDF selected")
        self.upload_button = QPushButton("Upload PDF")

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.file_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.file_label)
        layout.addWidget(self.upload_button)

        self.upload_button.clicked.connect(self.upload_requested.emit)

    def set_filename(self, filename: str | None) -> None:
        self.file_label.setText(filename if filename else "No PDF selected")