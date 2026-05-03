# models/response/extract_pdf_text_response.py

from dataclasses import dataclass


@dataclass
class ExtractPDFTextResponse:
    """Base response type for the extract_pdf_text tool."""
    pass


@dataclass
class ExtractPDFTextSuccessResponse(ExtractPDFTextResponse):
    path: str
    full_text: str
    page_count: int


@dataclass
class ExtractPDFTextErrorResponse(ExtractPDFTextResponse):
    error_type: str
    error_message: str