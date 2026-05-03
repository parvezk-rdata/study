# models/request/extract_pdf_text_request.py

from dataclasses import dataclass


@dataclass
class ExtractPDFTextRequest:
    pdf_path: str