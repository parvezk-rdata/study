from dataclasses import dataclass


@dataclass
class ClearConversationEvent:
    pass


@dataclass
class RemovePdfEvent:
    pass


@dataclass
class PdfUploadedEvent:
    filename: str
    pdf_bytes: bytes


@dataclass
class UserMessageSubmittedEvent:
    message: str