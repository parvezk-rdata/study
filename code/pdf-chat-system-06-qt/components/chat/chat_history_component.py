from PyQt6.QtCore import QEvent, QObject, QTimer
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from components.chat.chat_message_component import ChatMessageComponent


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
        self._create_widgets()
        self._build_layout()
        self._install_helpers()

    def _create_widgets(self) -> None:
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)

        self._container = QWidget()
        self._messages_layout = QVBoxLayout(self._container)
        self._messages_layout.setContentsMargins(8, 8, 8, 8)
        self._messages_layout.setSpacing(10)
        self._messages_layout.addStretch(1)

        self._scroll_area.setWidget(self._container)

    def _build_layout(self) -> None:
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._scroll_area)

    def _install_helpers(self) -> None:
        self._event_filter = _BottomScrollEventFilter(self)
        self._container.installEventFilter(self._event_filter)

    def get_scroll_area(self) -> QScrollArea:
        return self._scroll_area

    def get_container(self) -> QWidget:
        return self._container

    def get_messages_layout(self) -> QVBoxLayout:
        return self._messages_layout

    def clear_messages(self) -> None:
        while self._messages_layout.count() > 1:
            item = self._messages_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def add_message_item(self, header_text: str, content_text: str) -> None:
        widget = ChatMessageComponent()
        widget.set_header_text(header_text)
        widget.set_content_text(content_text)
        self._messages_layout.insertWidget(self._messages_layout.count() - 1, widget)

    def set_message_items(self, items: list[dict[str, str]]) -> None:
        self.clear_messages()
        for item in items:
            self.add_message_item(
                header_text=item.get("header", ""),
                content_text=item.get("content", ""),
            )
        self.scroll_to_bottom()

    def scroll_to_bottom(self) -> None:
        QTimer.singleShot(0, self._do_scroll_to_bottom)
        QTimer.singleShot(50, self._do_scroll_to_bottom)
        QTimer.singleShot(150, self._do_scroll_to_bottom)

    def _do_scroll_to_bottom(self) -> None:
        scrollbar = self._scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())