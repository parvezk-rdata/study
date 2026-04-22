from models.chat_models import ChatMessage
from services.llm_service import LLMService
from state.app_state_store import AppStateStore


class ChatController:
    def __init__(self, store: AppStateStore, llm_service: LLMService) -> None:
        self.store = store
        self.llm_service = llm_service

    def send_message(self, user_text: str) -> None:
        cleaned_text = user_text.strip()
        if not cleaned_text:
            self.store.set_status("Message is empty.")
            return

        state = self.store.get_state()
        if state.document is None:
            self.store.set_status("Upload a PDF first.")
            return

        prior_history = [
            {"role": msg.role, "content": msg.content} for msg in state.chat_history
        ]

        self.store.add_chat_message(ChatMessage(role="user", content=cleaned_text))
        self.store.set_status("Thinking...")

        try:
            reply = self.llm_service.chat(
                history=prior_history,
                pdf_text=state.document.text,
                user_msg=cleaned_text,
            )
        except RuntimeError as e:
            reply = f"Error: {e}"
        except Exception as e:
            reply = f"Error calling OpenAI: {e}"

        self.store.add_chat_message(ChatMessage(role="assistant", content=reply))
        self.store.set_status("Ready")