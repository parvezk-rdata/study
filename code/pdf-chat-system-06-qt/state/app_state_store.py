from PyQt6.QtCore import QObject, pyqtSignal

from models.chat_models import ChatMessage
from models.document_models import DocumentInfo
from state.app_state import AppState


class AppStateStore(QObject):
    document_changed = pyqtSignal(object)
    chat_changed = pyqtSignal(object)
    status_changed = pyqtSignal(str)
    state_changed = pyqtSignal(object)

    def __init__(self) -> None:
        super().__init__()
        self._state = AppState()

    def get_state(self) -> AppState:
        return self._state

    def set_document(self, document: DocumentInfo) -> None:
        self._state.document = document
        self.document_changed.emit(document)
        self.state_changed.emit(self._state)

    def clear_document(self) -> None:
        self._state.document = None
        self.document_changed.emit(None)
        self.state_changed.emit(self._state)

    def set_chat_history(self, history: list[ChatMessage]) -> None:
        self._state.chat_history = history
        self.chat_changed.emit(list(self._state.chat_history))
        self.state_changed.emit(self._state)

    def add_chat_message(self, message: ChatMessage) -> None:
        self._state.chat_history.append(message)
        self.chat_changed.emit(list(self._state.chat_history))
        self.state_changed.emit(self._state)

    def clear_chat(self) -> None:
        self._state.chat_history = []
        self.chat_changed.emit([])
        self.state_changed.emit(self._state)

    def set_status(self, message: str) -> None:
        self._state.status_message = message
        self.status_changed.emit(message)
        self.state_changed.emit(self._state)