import streamlit as st


class ChatView:
    def render(self, history: list[dict]) -> None:
        for msg in history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])