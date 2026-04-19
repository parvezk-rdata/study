from __future__ import annotations

import streamlit as st

from config import Settings
from services.pdf_service import PDFService
from state.doc_state import DocState
from state.chat_state import ChatState
from ui.pdf_panel import PDFPanelUI


class DocControllerLogic:
    """
    Handles PDF upload control flow:
    reading uploaded bytes, hash checking, extraction, and truncation warning.
    Reads and writes DocState and ChatState only.
    """

    def __init__(
        self,
        doc_state: DocState,
        chat_state: ChatState,
        pdf_svc: PDFService,
        pdf_ui: PDFPanelUI,
        config: Settings,
    ) -> None:
        self._doc_state = doc_state
        self._chat_state = chat_state
        self._pdf_svc = pdf_svc
        self._pdf_ui = pdf_ui
        self._config = config

    # ------------------------------------------------------------------
    # Upload handler
    # ------------------------------------------------------------------

    def handle_upload(self) -> None:
        pdf_bytes = self._pdf_ui.render_uploader(self._doc_state.get_uploader_key())

        if pdf_bytes is None:
            return

        if self._doc_state.is_same_file(pdf_bytes):
            doc = self._doc_state.get_doc()
        else:
            with st.spinner("Extracting text..."):
                try:
                    doc = self._pdf_svc.extract(pdf_bytes)
                except RuntimeError as e:
                    self._pdf_ui.render_extraction_error(str(e))
                    return

            self._doc_state.set_doc(doc, pdf_bytes)
            self._chat_state.clear_history()

        self._pdf_ui.render_metadata(
            page_count=doc.page_count,
            used_ocr=doc.used_ocr,
            char_count=doc.char_count,
        )

        if len(doc.text) > self._config.max_pdf_chars:
            self._pdf_ui.render_truncation_warning()
