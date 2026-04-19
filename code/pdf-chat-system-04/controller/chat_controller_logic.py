from __future__ import annotations

import streamlit as st

from config import Settings
from llm.openai_client import OpenAIClient
from llm.oauth_client import OAuthClient
from models.chat import Message
from services.auth_service import AuthService
from state.auth_state import AuthState
from state.chat_state import ChatState
from state.doc_state import DocState
from ui.chat_panel import ChatPanelUI


_SYSTEM_TEMPLATE = """You are an assistant that answers questions about the PDF provided below. Ground your answers in the PDF's content. If the answer isn't in the PDF, say so plainly rather than guessing.

<pdf>
{pdf_text}
</pdf>"""


class ChatControllerLogic:
    """
    Handles the full chat control flow:
    prompt building, client selection, LLM call, and state update.
    Reads AuthState, DocState, ChatState. Writes ChatState only.
    """

    def __init__(
        self,
        auth_state: AuthState,
        doc_state: DocState,
        chat_state: ChatState,
        chat_ui: ChatPanelUI,
        auth_svc: AuthService,
        config: Settings,
    ) -> None:
        self._auth_state = auth_state
        self._doc_state = doc_state
        self._chat_state = chat_state
        self._chat_ui = chat_ui
        self._auth_svc = auth_svc
        self._config = config

    # ------------------------------------------------------------------
    # Chat handler
    # ------------------------------------------------------------------

    def handle_chat(self) -> None:
        doc = self._doc_state.get_doc()
        history = self._chat_state.get_history()

        self._chat_ui.render_history(history)
        prompt = self._chat_ui.render_chat_input(doc_ready=doc is not None)

        if not prompt:
            return

        if doc is None:
            self._chat_ui.render_no_pdf_warning()
            return

        pdf_text = self._trim_pdf(doc.text)

        self._chat_ui.render_user_message(prompt)

        with self._chat_ui.thinking_spinner():
            try:
                reply = self._call_llm(history, pdf_text, prompt)
            except RuntimeError as e:
                reply = f"**Error:** {e}"
            except Exception as e:
                reply = f"**Unexpected error:** {e}"

        self._chat_ui.render_assistant_reply(reply)
        self._chat_state.append_message("user", prompt)
        self._chat_state.append_message("assistant", reply)

    # ------------------------------------------------------------------
    # Private — LLM dispatch
    # ------------------------------------------------------------------

    def _call_llm(
        self, history: list[Message], pdf_text: str, prompt: str
    ) -> str:
        client = self._pick_client()

        if isinstance(client, OpenAIClient):
            messages = self._build_openai_messages(history, pdf_text, prompt)
            return client.chat(messages)

        if isinstance(client, OAuthClient):
            instructions = self._build_system_prompt(pdf_text)
            input_items = self._build_oauth_items(history, prompt)
            return client.chat(instructions, input_items)

        raise RuntimeError("Unknown LLM client type.")

    def _pick_client(self) -> OpenAIClient | OAuthClient:
        stored = self._auth_svc.load_stored_auth()
        if self._auth_state.is_oauth_mode() and stored is not None:
            stored = self._auth_svc.refresh_if_needed(stored)
            oauth_model = (
                self._auth_state.get_oauth_model() or self._config.default_oauth_model
            )
            # Pass oauth_model via a config override at call time
            return OAuthClient(self._config, stored)
        return OpenAIClient(self._config)

    # ------------------------------------------------------------------
    # Private — prompt building
    # ------------------------------------------------------------------

    def _trim_pdf(self, pdf_text: str) -> str:
        max_chars = self._config.max_pdf_chars
        return pdf_text[:max_chars] if len(pdf_text) > max_chars else pdf_text

    def _build_system_prompt(self, pdf_text: str) -> str:
        return _SYSTEM_TEMPLATE.format(pdf_text=pdf_text)

    def _build_openai_messages(
        self, history: list[Message], pdf_text: str, prompt: str
    ) -> list[Message]:
        system = Message(role="user", content=self._build_system_prompt(pdf_text))
        user = Message(role="user", content=prompt)
        return [system, *history, user]

    def _build_oauth_items(
        self, history: list[Message], prompt: str
    ) -> list[dict]:
        items = [msg.to_responses_item() for msg in history]
        items.append(Message(role="user", content=prompt).to_responses_item())
        return items
