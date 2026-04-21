from PyQt6.QtCore import QEvent, QObject, QTimer
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from components.chat.chat_message_component import ChatMessageComponent
from models.chat_models import ChatMessage


class _BottomScrollEventFilter(QObject):
    def __init__(self, owner: "ChatHistoryComponent") -> None:
        super().__init__()
        self.owner = owner

    def eventFilter(self, watched, event):
        if event.type() in (
            QEvent.Type.Resize,
            QEvent.Type.LayoutRequest,
            QEvent.Type.Show,
        ):
            self.owner._do_scroll_to_bottom()
        return super().eventFilter(watched, event)


class ChatHistoryComponent(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container = QWidget()
        self.messages_layout = QVBoxLayout(self.container)
        self.messages_layout.setContentsMargins(8, 8, 8, 8)
        self.messages_layout.setSpacing(10)
        self.messages_layout.addStretch(1)

        self.scroll_area.setWidget(self.container)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll_area)

        self._event_filter = _BottomScrollEventFilter(self)
        self.container.installEventFilter(self._event_filter)

    def set_messages(self, messages: list[ChatMessage]) -> None:
        self._clear_messages()

        for message in messages:
            widget = ChatMessageComponent(message)
            self.messages_layout.insertWidget(self.messages_layout.count() - 1, widget)

        self._scroll_to_bottom()

    def _clear_messages(self) -> None:
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _scroll_to_bottom(self) -> None:
        QTimer.singleShot(0, self._do_scroll_to_bottom)
        QTimer.singleShot(50, self._do_scroll_to_bottom)
        QTimer.singleShot(150, self._do_scroll_to_bottom)

    def _do_scroll_to_bottom(self) -> None:
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())