import hashlib
from pathlib import Path

from models.document_models import DocumentInfo
from services.llm_service import LLMService
from services.pdf_extraction_service import PDFExtractionService
from state.app_state_store import AppStateStore


class DocumentController:
    def __init__(
        self,
        store: AppStateStore,
        pdf_service: PDFExtractionService,
        llm_service: LLMService,
    ) -> None:
        self.store = store
        self.pdf_service = pdf_service
        self.llm_service = llm_service

    def _file_hash(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def load_pdf(self, file_path: str) -> None:
        path = Path(file_path)
        pdf_bytes = path.read_bytes()
        file_hash = self._file_hash(pdf_bytes)

        current_doc = self.store.get_state().document
        if current_doc and current_doc.file_hash == file_hash:
            self.store.set_status("Same PDF is already loaded.")
            return

        self.store.set_status("Extracting text from PDF...")

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

        self.store.set_document(document)
        self.store.clear_chat()
        self.store.set_status(f"Loaded PDF: {document.filename}")

    def remove_pdf(self) -> None:
        self.store.clear_document()
        self.store.clear_chat()
        self.store.set_status("PDF removed.")