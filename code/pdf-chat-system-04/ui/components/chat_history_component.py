import streamlit as st


class ChatHistoryComponent:
    def render(self, history: list[dict]) -> None:
        for msg in history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])