from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from components.chat.chat_history_component import ChatHistoryComponent
from components.chat.chat_input_component import ChatInputComponent
from components.document.pdf_panel_component import PDFPanelComponent


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Chat with a PDF")
        self.resize(1100, 700)

        self.pdf_panel_component = PDFPanelComponent()

        self.chat_history_component = ChatHistoryComponent()
        self.chat_input_component = ChatInputComponent()

        self.clear_chat_button = QPushButton("Clear conversation")
        self.remove_pdf_button = QPushButton("Remove PDF")

        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        sidebar = self._build_sidebar()
        main_area = self._build_main_area()

        root_layout.addWidget(sidebar, 0)
        root_layout.addWidget(main_area, 1)

        self.statusBar().showMessage("Ready")

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar.setFixedWidth(290)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        layout.addWidget(self.pdf_panel_component)
        layout.addWidget(self.clear_chat_button)
        layout.addWidget(self.remove_pdf_button)
        layout.addStretch(1)

        return sidebar

    def _build_main_area(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(self.chat_history_component, 1)
        layout.addWidget(self.chat_input_component, 0)

        return panel