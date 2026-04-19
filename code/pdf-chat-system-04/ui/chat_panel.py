from __future__ import annotations

from contextlib import contextmanager

import streamlit as st

from models.chat import Message


class ChatPanelUI:
    """
    Renders all chat-related UI components.
    Completely stateless — receives history and messages as arguments,
    returns the raw prompt string typed by the user.
    """

    def render_history(self, history: list[Message]) -> None:
        for msg in history:
            with st.chat_message(msg.role):
                st.markdown(msg.content)

    def render_chat_input(self, doc_ready: bool) -> str | None:
        placeholder = (
            "Ask a question about the PDF" if doc_ready else "Upload a PDF to start"
        )
        return st.chat_input(placeholder)

    def render_user_message(self, prompt: str) -> None:
        with st.chat_message("user"):
            st.markdown(prompt)

    def render_assistant_reply(self, reply: str) -> None:
        with st.chat_message("assistant"):
            st.markdown(reply)

    def render_no_pdf_warning(self) -> None:
        st.warning("Upload a PDF first.")

    @contextmanager
    def thinking_spinner(self):
        with st.spinner("Thinking..."):
            yield
