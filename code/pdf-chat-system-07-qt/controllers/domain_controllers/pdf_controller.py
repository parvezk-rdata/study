import hashlib
from pathlib import Path

from controllers.controller_results import PDFLoadResult
from models.document_models import DocumentInfo
from services.llm_service import LLMService
from services.pdf_extraction_service import PDFExtractionService


class PDFController:
    def __init__(
        self,
        pdf_service: PDFExtractionService,
        llm_service: LLMService,
    ) -> None:
        self.pdf_service = pdf_service
        self.llm_service = llm_service

    def load_pdf(
        self,
        file_path: str,
        current_document: DocumentInfo | None,
    ) -> PDFLoadResult:
        try:
            path = Path(file_path)
            pdf_bytes = path.read_bytes()
            file_hash = self._file_hash(pdf_bytes)

            if current_document and current_document.file_hash == file_hash:
                return PDFLoadResult(
                    success=False,
                    document=current_document,
                    status_message="Same PDF is already loaded.",
                    reset_chat=False,
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

            return PDFLoadResult(
                success=True,
                document=document,
                status_message=f"Loaded PDF: {document.filename}",
                reset_chat=True,
            )
        except Exception as e:
            return PDFLoadResult(
                success=False,
                document=current_document,
                status_message=f"Error loading PDF: {e}",
                reset_chat=False,
            )

    def remove_pdf(self) -> str:
        return "PDF removed."

    def _file_hash(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()