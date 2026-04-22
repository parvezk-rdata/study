from models.chat_models import ChatMessage
from models.document_models import DocumentInfo
from services.llm_service import LLMService


class ChatController:
    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def normalize_user_text(self, user_text: str) -> str:
        return user_text.strip()

    def build_reply(
        self,
        history: list[ChatMessage],
        document: DocumentInfo,
        user_text: str,
    ) -> str:
        prior_history = [
            {"role": message.role, "content": message.content} for message in history
        ]

        return self.llm_service.chat(
            history=prior_history,
            pdf_text=document.text,
            user_msg=user_text,
        )