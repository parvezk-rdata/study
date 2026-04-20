from pdf_extractor import ExtractedDoc
from ui.sidebar_view import SidebarView
from ui.document_view import DocumentView
from ui.chat_view import ChatView
from ui.input_view import ChatInputView
from ui.main_view import MainView


class UIController:
    def __init__(self) -> None:
        self.main_view = MainView()
        self.sidebar_view = SidebarView()
        self.document_view = DocumentView()
        self.chat_view = ChatView()
        self.input_view = ChatInputView()

    def render_sidebar(self) -> str | None:
        return self.sidebar_view.render()

    def render_document_uploader(self, uploader_key: int):
        return self.document_view.render_uploader(uploader_key)

    def render_document_summary(
        self,
        filename: str | None,
        doc: ExtractedDoc,
        is_truncated: bool,
    ) -> None:
        self.document_view.render_summary(filename, doc, is_truncated)

    def render_chat_history(self, history: list[dict]) -> None:
        self.chat_view.render(history)

    def render_chat_input(self, has_document: bool) -> str | None:
        return self.input_view.render(has_document)