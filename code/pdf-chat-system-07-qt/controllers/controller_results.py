from dataclasses import dataclass
from typing import Optional

from models.document_models import DocumentInfo


@dataclass
class PDFLoadResult:
    success: bool
    document: Optional[DocumentInfo]
    status_message: str
    reset_chat: bool


@dataclass
class LLMChatResult:
    success: bool
    user_message: Optional[str]
    assistant_message: Optional[str]
    status_message: str