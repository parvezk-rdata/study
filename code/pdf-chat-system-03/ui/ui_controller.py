from pdf_extractor import ExtractedDoc
from ui.components.sidebar_component import SidebarComponent
from ui.components.uploader_component import UploaderComponent
from ui.components.document_info_component import DocumentInfoComponent
from ui.components.chat_history_component import ChatHistoryComponent
from ui.components.chat_input_component import ChatInputComponent


class UIController:
    def __init__(self) -> None:
        self.sidebar = SidebarComponent()
        self.uploader = UploaderComponent()
        self.document_info = DocumentInfoComponent()
        self.chat_history = ChatHistoryComponent()
        self.chat_input = ChatInputComponent()

    def render_sidebar(self) -> str | None:
        return self.sidebar.render()

    def render_uploader(self, uploader_key: int):
        return self.uploader.render(uploader_key)

    def render_document_info(
        self,
        filename: str | None,
        doc: ExtractedDoc,
        is_truncated: bool,
    ) -> None:
        self.document_info.render(filename, doc, is_truncated)

    def render_chat_history(self, history: list[dict]) -> None:
        self.chat_history.render(history)

    def render_chat_input(self, has_document: bool) -> str | None:
        return self.chat_input.render(has_document)