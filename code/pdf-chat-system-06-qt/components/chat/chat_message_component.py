from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ChatMessageComponent(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._create_widgets()
        self._build_layout()

    def _create_widgets(self) -> None:
        self._header_label = QLabel()
        self._content_label = QLabel()

        self._header_label.setWordWrap(True)
        self._content_label.setWordWrap(True)
        self._content_label.setTextInteractionFlags(
            self._content_label.textInteractionFlags()
        )

    def _build_layout(self) -> None:
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(4)

        self._layout.addWidget(self._header_label)
        self._layout.addWidget(self._content_label)

    def get_header_label(self) -> QLabel:
        return self._header_label

    def get_content_label(self) -> QLabel:
        return self._content_label

    def set_header_text(self, text: str) -> None:
        self._header_label.setText(text)

    def set_content_text(self, text: str) -> None:
        self._content_label.setText(text)

    def get_header_text(self) -> str:
        return self._header_label.text()

    def get_content_text(self) -> str:
        return self._content_label.text()