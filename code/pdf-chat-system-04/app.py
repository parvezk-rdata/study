import streamlit as st

from controllers.main_controller import MainController
from ui.ui_controller import UIController
from ui.ui_state_store import UIStateStore


class App:
    def __init__(self) -> None:
        self.store = UIStateStore()
        self.ui = UIController()
        self.controller = MainController(self.store)

    def setup_page(self) -> None:
        st.set_page_config(page_title="PDF Chat", page_icon="📄")
        st.title("Chat with a PDF")

    def run(self) -> None:
        self.setup_page()
        self.store.init_state()

        top_events = self.ui.collect_top_events(
            uploader_key=self.store.get_uploader_key(),
        )

        for event in top_events:
            self.controller.handle_event(event)

        doc = self.store.get_doc()
        if doc is not None:
            self.ui.render_document_info(
                filename=self.store.get_doc_name(),
                doc=doc,
                is_truncated=self.store.get_is_truncated(),
            )

        self.ui.render_chat_history(self.store.get_history())

        chat_event = self.ui.collect_chat_event(
            has_document=doc is not None,
        )
        if chat_event is not None:
            self.controller.handle_event(chat_event)


if __name__ == "__main__":
    App().run()