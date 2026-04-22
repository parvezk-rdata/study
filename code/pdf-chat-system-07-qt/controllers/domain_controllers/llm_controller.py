from controllers.controller_results import LLMChatResult
from models.chat_models import ChatMessage
from models.document_models import DocumentInfo
from services.llm_service import LLMService


class LLMController:
    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def send_message(
        self,
        user_text: str,
        current_document: DocumentInfo | None,
        chat_history: list[ChatMessage],
    ) -> LLMChatResult:
        cleaned_text = user_text.strip()

        if not cleaned_text:
            return LLMChatResult(
                success=False,
                user_message=None,
                assistant_message=None,
                status_message="Message is empty.",
            )

        if current_document is None:
            return LLMChatResult(
                success=False,
                user_message=None,
                assistant_message=None,
                status_message="Upload a PDF first.",
            )

        prior_history = [
            {"role": message.role, "content": message.content}
            for message in chat_history
        ]

        try:
            reply = self.llm_service.chat(
                history=prior_history,
                pdf_text=current_document.text,
                user_msg=cleaned_text,
            )
            return LLMChatResult(
                success=True,
                user_message=cleaned_text,
                assistant_message=reply,
                status_message="Ready",
            )
        except RuntimeError as e:
            return LLMChatResult(
                success=True,
                user_message=cleaned_text,
                assistant_message=f"Error: {e}",
                status_message="Ready",
            )
        except Exception as e:
            return LLMChatResult(
                success=True,
                user_message=cleaned_text,
                assistant_message=f"Error calling OpenAI: {e}",
                status_message="Ready",
            )