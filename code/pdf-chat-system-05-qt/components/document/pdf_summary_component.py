from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PDFSummaryComponent(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.summary_label = QLabel("Upload a PDF to start chatting.")
        self.summary_label.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(self.summary_label)

    def set_summary(self, text: str) -> None:
        self.summary_label.setText(text)

    def clear_summary(self) -> None:
        self.summary_label.setText("Upload a PDF to start chatting.")