from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from models.document_models import DocumentInfo


class PDFInfoComponent(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.title_label = QLabel("PDF Info")
        self.info_label = QLabel("No PDF loaded")

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.info_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.info_label)

    def set_document(self, document: DocumentInfo | None) -> None:
        if document is None:
            self.info_label.setText("No PDF loaded")
            return

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