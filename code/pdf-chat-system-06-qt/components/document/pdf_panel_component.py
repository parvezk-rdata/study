from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from models.document_models import DocumentInfo


class PDFPanelComponent(QWidget):
    upload_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.title_label = QLabel("PDF")
        self.file_label = QLabel("No PDF selected")
        self.upload_button = QPushButton("Upload PDF")
        self.info_label = QLabel("Upload a PDF to start chatting.")

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.file_label.setWordWrap(True)
        self.info_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.file_label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.info_label)

        self.upload_button.clicked.connect(self.upload_requested.emit)

    def set_document(self, document: DocumentInfo | None) -> None:
        if document is None:
            self.file_label.setText("No PDF selected")
            self.info_label.setText("Upload a PDF to start chatting.")
            return

        self.file_label.setText(document.filename)

        warning = ""
        if document.truncated:
            warning = (
                "\n\nWarning: PDF exceeds the context budget. "
                "Later pages will be truncated during chat."
            )

        self.info_label.setText(
            f"Pages: {document.page_count}\n"
            f"Method: {document.extraction_method}\n"
            f"Characters: {document.char_count:,}"
            f"{warning}"
        )