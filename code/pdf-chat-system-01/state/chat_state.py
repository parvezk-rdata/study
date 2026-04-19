from __future__ import annotations

import streamlit as st

from models.chat import Message


class ChatState:
    """Manages all chat-related entries in st.session_state."""

    def init(self) -> None:
        st.session_state.setdefault("history", [])

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def get_history(self) -> list[Message]:
        return st.session_state.get("history", [])

    def append_message(self, role: str, content: str) -> None:
        st.session_state["history"].append(Message(role=role, content=content))

    def clear_history(self) -> None:
        st.session_state["history"] = []
