from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from models.chat_models import ChatMessage


class ChatMessageComponent(QWidget):
    def __init__(self, message: ChatMessage) -> None:
        super().__init__()
        self.message = message

        self.role_label = QLabel(self._display_role(message.role))
        self.content_label = QLabel(message.content)

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        self.role_label.setStyleSheet("font-weight: bold;")
        self.content_label.setWordWrap(True)
        self.content_label.setTextInteractionFlags(
            self.content_label.textInteractionFlags()
        )

        layout.addWidget(self.role_label)
        layout.addWidget(self.content_label)

    def _display_role(self, role: str) -> str:
        if role == "user":
            return "You"
        if role == "assistant":
            return "Assistant"
        return role.capitalize()