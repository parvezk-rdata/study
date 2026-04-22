from PyQt6.QtWidgets import QFrame, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from components.chat.chat_history_component import ChatHistoryComponent
from components.chat.chat_input_component import ChatInputComponent
from components.document.pdf_panel_component import PDFPanelComponent


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._create_widgets()
        self._build_ui()

    def _create_widgets(self) -> None:
        self._pdf_panel_component = PDFPanelComponent()
        self._chat_history_component = ChatHistoryComponent()
        self._chat_input_component = ChatInputComponent()

    def _build_ui(self) -> None:
        self.setWindowTitle("PDF Chat")
        self.resize(1100, 700)

        self._central = QWidget()
        self.setCentralWidget(self._central)

        self._root_layout = QHBoxLayout(self._central)
        self._root_layout.setContentsMargins(12, 12, 12, 12)
        self._root_layout.setSpacing(12)

        self._sidebar = self._build_sidebar()
        self._main_area = self._build_main_area()

        self._root_layout.addWidget(self._sidebar, 0)
        self._root_layout.addWidget(self._main_area, 1)

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar.setFixedWidth(290)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        layout.addWidget(self._pdf_panel_component)
        layout.addStretch(1)

        return sidebar

    def _build_main_area(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(self._chat_history_component, 1)
        layout.addWidget(self._chat_input_component, 0)

        return panel

    def get_pdf_panel_component(self) -> PDFPanelComponent:
        return self._pdf_panel_component

    def get_chat_history_component(self) -> ChatHistoryComponent:
        return self._chat_history_component

    def get_chat_input_component(self) -> ChatInputComponent:
        return self._chat_input_component