import streamlit as st
from pdf_extractor import ExtractedDoc


class DocumentView:
    def render_uploader(self, uploader_key: int):
        return st.file_uploader(
            "Upload a PDF",
            type=["pdf"],
            key=f"uploader_{uploader_key}",
        )

    def render_summary(
        self,
        filename: str | None,
        doc: ExtractedDoc,
        is_truncated: bool,
    ) -> None:
        method = "OCR" if doc.used_ocr else "PyPDF"

        if filename:
            st.subheader(filename)

        st.caption(
            f"{doc.page_count} pages · extracted via {method} · {len(doc.text):,} chars"
        )

        if is_truncated:
            st.warning(
                "PDF exceeds the context budget; later pages were truncated. "
                "v1 has no retrieval — consider a smaller PDF."
            )