import hashlib
from pathlib import Path
from typing import Optional

from controllers.controller_results import LoadPDFResult
from models.document_models import DocumentInfo
from services.llm_service import LLMService
from services.pdf_extraction_service import PDFExtractionService


class DocumentController:
    def __init__(
        self,
        pdf_service: PDFExtractionService,
        llm_service: LLMService,
    ) -> None:
        self.pdf_service = pdf_service
        self.llm_service = llm_service

    def _file_hash(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def load_pdf(
        self,
        file_path: str,
        current_document: Optional[DocumentInfo],
    ) -> LoadPDFResult:
        path = Path(file_path)
        pdf_bytes = path.read_bytes()
        file_hash = self._file_hash(pdf_bytes)

        if current_document and current_document.file_hash == file_hash:
            return LoadPDFResult(
                document=current_document,
                status_message="Same PDF is already loaded.",
                is_same_document=True,
            )

        extracted = self.pdf_service.extract(pdf_bytes)
        truncated = self.llm_service.is_truncated(extracted.text)

        document = DocumentInfo(
            filename=path.name,
            file_hash=file_hash,
            text=extracted.text,
            page_count=extracted.page_count,
            used_ocr=extracted.used_ocr,
            char_count=len(extracted.text),
            truncated=truncated,
        )

        return LoadPDFResult(
            document=document,
            status_message=f"Loaded PDF: {document.filename}",
            is_same_document=False,
        )