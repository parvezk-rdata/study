# controllers/extract_pdf_text_controller.py

from pathlib import Path
from services.pdf_validator import PDFValidator
from services.pdf_reader import PDFReader
from models.request.extract_pdf_text_request import ExtractPDFTextRequest
from models.response.extract_pdf_text_response import (
    ExtractPDFTextResponse,
    ExtractPDFTextSuccessResponse,
    ExtractPDFTextErrorResponse,
)


class ExtractPDFTextController:

    def __init__(self):
        self._validator = PDFValidator()
        self._reader = PDFReader()

    def execute(self, request: ExtractPDFTextRequest) -> ExtractPDFTextResponse:
        error = self._validator.validate(request.pdf_path)
        if error:
            return ExtractPDFTextErrorResponse(
                error_type="ValidationError",
                error_message=error,
            )

        path = Path(request.pdf_path).expanduser().resolve()
        try:
            full_text, page_count = self._reader.read(path)
        except Exception as exc:
            return ExtractPDFTextErrorResponse(
                error_type="ExtractionError",
                error_message=f"Failed to extract text from PDF: {exc}",
            )

        return ExtractPDFTextSuccessResponse(
            path=str(path),
            full_text=full_text,
            page_count=page_count,
        )
