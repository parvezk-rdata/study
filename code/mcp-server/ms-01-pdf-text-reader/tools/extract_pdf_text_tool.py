# tools/extract_pdf_text_tool.py

from controllers.extract_pdf_text_controller import ExtractPDFTextController
from models.request.extract_pdf_text_request import ExtractPDFTextRequest
from models.response.extract_pdf_text_response import (
    ExtractPDFTextSuccessResponse,
    ExtractPDFTextErrorResponse,
)


controller = ExtractPDFTextController()


def extract_pdf_text(pdf_path: str) -> dict:
    """Extract all text from a PDF file and return it with metadata."""

    request = ExtractPDFTextRequest(pdf_path=pdf_path)
    response = controller.execute(request)

    if isinstance(response, ExtractPDFTextErrorResponse):
        return {
            "success": False,
            "error_type": response.error_type,
            "error_message": response.error_message,
        }

    if isinstance(response, ExtractPDFTextSuccessResponse):
        return {
            "success": True,
            "path": response.path,
            "full_text": response.full_text,
            "page_count": response.page_count,
        }
