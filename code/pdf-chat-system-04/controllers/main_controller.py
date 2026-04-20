import hashlib
import streamlit as st

from llm_client import chat, fit_pdf_to_context
from pdf_extractor import extract
from ui.events import (
    ClearConversationEvent,
    PdfUploadedEvent,
    RemovePdfEvent,
    UserMessageSubmittedEvent,
)
from ui.ui_state_store import UIStateStore


class MainController:
    def __init__(self, store: UIStateStore) -> None:
        self.store = store

    def handle_event(self, event) -> None:
        if isinstance(event, ClearConversationEvent):
            self.handle_clear_conversation()
        elif isinstance(event, RemovePdfEvent):
            self.handle_remove_pdf()
        elif isinstance(event, PdfUploadedEvent):
            self.handle_pdf_uploaded(event)
        elif isinstance(event, UserMessageSubmittedEvent):
            self.handle_user_message(event)

    def handle_clear_conversation(self) -> None:
        self.store.clear_conversation()
        st.rerun()

    def handle_remove_pdf(self) -> None:
        self.store.remove_pdf()
        st.rerun()

    def handle_pdf_uploaded(self, event: PdfUploadedEvent) -> None:
        current_hash = self._file_hash(event.pdf_bytes)

        if self.store.get_doc_hash() == current_hash:
            return

        with st.spinner("Extracting text..."):
            try:
                doc = extract(event.pdf_bytes)
            except RuntimeError as e:
                st.error(str(e))
                return

        _, truncated = fit_pdf_to_context(doc.text)

        self.store.set_doc(doc)
        self.store.set_doc_hash(current_hash)
        self.store.set_doc_name(event.filename)
        self.store.set_is_truncated(truncated)
        self.store.clear_conversation()

        st.rerun()

    def handle_user_message(self, event: UserMessageSubmittedEvent) -> None:
        doc = self.store.get_doc()

        if doc is None:
            st.warning("Upload a PDF first.")
            return

        prompt = event.message.strip()
        if not prompt:
            return

        prior_history = list(self.store.get_history())
        self.store.append_message("user", prompt)

        with st.spinner("Thinking..."):
            try:
                reply = chat(prior_history, doc.text, prompt)
            except RuntimeError as e:
                reply = f"**Error:** {e}"
            except Exception as e:
                reply = f"**Error calling OpenAI:** {e}"

        self.store.append_message("assistant", reply)
        st.rerun()

    @staticmethod
    def _file_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()