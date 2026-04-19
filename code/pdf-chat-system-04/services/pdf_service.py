from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader

from models.doc import ExtractedDoc


class PDFService:
    """Extracts text from raw PDF bytes. Raises RuntimeError on failure."""

    _MIN_CHARS_PER_PAGE = 10

    def extract(self, pdf_bytes: bytes) -> ExtractedDoc:
        reader = PdfReader(BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        text = "\n\n".join(
            page.extract_text() or "" for page in reader.pages
        ).strip()

        if page_count > 0 and len(text) >= page_count * self._MIN_CHARS_PER_PAGE:
            return ExtractedDoc(text=text, page_count=page_count, used_ocr=False)

        ocr_text = self._ocr_extract(pdf_bytes, page_count)
        return ExtractedDoc(text=ocr_text, page_count=page_count, used_ocr=True)

    # ------------------------------------------------------------------
    # OCR fallback
    # ------------------------------------------------------------------

    def _ocr_extract(self, pdf_bytes: bytes, page_count: int) -> str:
        try:
            from pdf2image import convert_from_bytes
            import pytesseract
        except ImportError as e:
            raise RuntimeError(
                "OCR fallback needs `pdf2image` and `pytesseract`. "
                "Install with `pip install pdf2image pytesseract`."
            ) from e

        try:
            images = convert_from_bytes(pdf_bytes)
        except Exception as e:
            raise RuntimeError(
                "OCR fallback failed while rasterizing the PDF. "
                "On macOS: `brew install poppler`."
            ) from e

        pages: list[str] = []
        for img in images:
            try:
                pages.append(pytesseract.image_to_string(img))
            except pytesseract.TesseractNotFoundError as e:
                raise RuntimeError(
                    "Tesseract binary not found. On macOS: `brew install tesseract`."
                ) from e

        return "\n\n".join(pages).strip()
