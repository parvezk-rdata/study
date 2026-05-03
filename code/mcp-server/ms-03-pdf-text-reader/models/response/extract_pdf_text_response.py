# models/response/extract_pdf_text_response.py

from pydantic import BaseModel


class ExtractPDFTextResponse(BaseModel):
    success: bool
    pdf_path: str | None = None

    full_text: str | None = None
    page_count: int | None = None

    error_type: str | None = None
    error_message: str | None = None