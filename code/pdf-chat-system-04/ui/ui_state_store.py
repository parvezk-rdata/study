
'''

| State Key      | Type         | Purpose                                                   |
|----------------|------------  |-----------------------------------------------------------|
| history        | list         | display chat messages, send past conversation to LLM      |
|----------------|------------  |-----------------------------------------------------------|
| uploader_key   | int          | Forces file uploader to reset when PDF is removed         |
|----------------|------------  |-----------------------------------------------------------|
| doc            | ExtractedDoc | Stores PDF data(text, total page). pass text to LLM       |
|----------------|------------  |-----------------------------------------------------------|
| doc_hash       | str          | PDF hash. detects new PDF. triggers reset when PDF changes|
|----------------|------------  |-----------------------------------------------------------|
| doc_name       | str          | Used to display filename in UI                            |
|----------------|------------  |-----------------------------------------------------------|

'''

import streamlit as st
from pdf_extractor import ExtractedDoc


class UIStateStore:
    def init_state(self) -> None:
        # first run :   key does not exist then create them
        # re-run    :   key already exists then retain old keys
        st.session_state.setdefault("history", [])
        st.session_state.setdefault("uploader_key", 0)
        st.session_state.setdefault("doc", None)
        st.session_state.setdefault("doc_hash", None)
        st.session_state.setdefault("doc_name", None)
        st.session_state.setdefault("is_truncated", False)

    def get_history(self) -> list[dict]:
        return st.session_state["history"]

    def set_history(self, history: list[dict]) -> None:
        st.session_state["history"] = history

    def append_message(self, role: str, content: str) -> None:
        st.session_state["history"].append(
            {"role": role, "content": content}
        )

    def clear_conversation(self) -> None:
        st.session_state["history"] = []

    def get_doc(self) -> ExtractedDoc | None:
        return st.session_state.get("doc")

    def set_doc(self, doc: ExtractedDoc | None) -> None:
        st.session_state["doc"] = doc

    def get_doc_hash(self) -> str | None:
        return st.session_state.get("doc_hash")

    def set_doc_hash(self, doc_hash: str | None) -> None:
        st.session_state["doc_hash"] = doc_hash

    def get_doc_name(self) -> str | None:
        return st.session_state.get("doc_name")

    def set_doc_name(self, doc_name: str | None) -> None:
        st.session_state["doc_name"] = doc_name

    def get_is_truncated(self) -> bool:
        return st.session_state["is_truncated"]

    def set_is_truncated(self, is_truncated: bool) -> None:
        st.session_state["is_truncated"] = is_truncated

    def get_uploader_key(self) -> int:
        return st.session_state["uploader_key"]

    def increment_uploader_key(self) -> None:
        st.session_state["uploader_key"] += 1

    def remove_pdf(self) -> None:
        st.session_state["doc"] = None
        st.session_state["doc_hash"] = None
        st.session_state["doc_name"] = None
        st.session_state["is_truncated"] = False
        st.session_state["history"] = []
        st.session_state["uploader_key"] += 1