from pdf_extractor import ExtractedDoc
from ui.components.chat_history_component import ChatHistoryComponent
from ui.components.chat_input_component import ChatInputComponent
from ui.components.document_info_component import DocumentInfoComponent
from ui.components.sidebar_component import SidebarComponent
from ui.components.uploader_component import UploaderComponent
from ui.events import PdfUploadedEvent, UserMessageSubmittedEvent
from ui.ui_state_store import UIStateStore


class UIController:
    def __init__(self) -> None:
        self.sidebar = SidebarComponent()
        self.uploader = UploaderComponent()
        self.document_info = DocumentInfoComponent()
        self.chat_history = ChatHistoryComponent()
        self.chat_input = ChatInputComponent()

    def collect_events(self, has_document: bool) -> list:
        events = []

        sidebar_event = self.sidebar.render()
        if sidebar_event is not None:
            events.append(sidebar_event)

        uploaded_file = self.uploader.render(UIStateStore().get_uploader_key())
        if uploaded_file is not None:
            events.append(
                PdfUploadedEvent(
                    filename=uploaded_file.name,
                    pdf_bytes=uploaded_file.getvalue(),
                )
            )

        prompt = self.chat_input.render(has_document=has_document)
        if prompt:
            events.append(UserMessageSubmittedEvent(message=prompt))

        return events

    def render_document_info(
        self,
        filename: str | None,
        doc: ExtractedDoc,
        is_truncated: bool,
    ) -> None:
        self.document_info.render(filename, doc, is_truncated)

    def render_chat_history(self, history: list[dict]) -> None:
        self.chat_history.render(history)