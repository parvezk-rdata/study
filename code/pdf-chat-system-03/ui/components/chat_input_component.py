import streamlit as st


class ChatInputComponent:
    def render(self, has_document: bool) -> str | None:
        placeholder = (
            "Ask a question about the PDF"
            if has_document
            else "Upload a PDF to start"
        )
        return st.chat_input(placeholder)