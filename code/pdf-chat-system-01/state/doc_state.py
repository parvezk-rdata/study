from __future__ import annotations

import hashlib

import streamlit as st

from models.doc import ExtractedDoc


class DocState:
    """Manages all document-related entries in st.session_state."""

    def init(self) -> None:
        st.session_state.setdefault("doc", None)
        st.session_state.setdefault("doc_hash", None)
        st.session_state.setdefault("uploader_key", 0)

    # ------------------------------------------------------------------
    # Document
    # ------------------------------------------------------------------

    def get_doc(self) -> ExtractedDoc | None:
        return st.session_state.get("doc")

    def set_doc(self, doc: ExtractedDoc, raw_bytes: bytes) -> None:
        st.session_state["doc"] = doc
        st.session_state["doc_hash"] = self._compute_hash(raw_bytes)

    def clear_doc(self) -> None:
        st.session_state["doc"] = None
        st.session_state["doc_hash"] = None
        self._increment_uploader_key()

    # ------------------------------------------------------------------
    # Hash
    # ------------------------------------------------------------------

    def is_same_file(self, raw_bytes: bytes) -> bool:
        current = st.session_state.get("doc_hash")
        return current is not None and current == self._compute_hash(raw_bytes)

    # ------------------------------------------------------------------
    # Uploader key
    # ------------------------------------------------------------------

    def get_uploader_key(self) -> int:
        return st.session_state.get("uploader_key", 0)

    def _increment_uploader_key(self) -> None:
        st.session_state["uploader_key"] = self.get_uploader_key() + 1

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()
