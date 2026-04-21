from dataclasses import dataclass, field
from typing import Optional

from models.chat_models import ChatMessage
from models.document_models import DocumentInfo


@dataclass
class AppState:
    document: Optional[DocumentInfo] = None
    chat_history: list[ChatMessage] = field(default_factory=list)
    status_message: str = ""