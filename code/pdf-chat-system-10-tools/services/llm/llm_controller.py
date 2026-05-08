# services/llm/llm_controller.py

from typing import Any

from services.llm.llm_service import LLMService
from app.models.services.llm_transaction.chat_message import ChatMessage


class LLMController:
    """
    Builds and manages OpenAI message payloads.

    Responsibilities:
    - build running conversation messages
    - call LLMService with or without tools
    - parse LLM response
    - store error state if LLM call fails

    Not responsible for:
    - calling MCP server
    - executing tools
    """

    def __init__( self, llm_service: LLMService, mcp_tools: list[dict], system_prompt: str ):

        self._llm_service = llm_service
        self._mcp_tools = mcp_tools
        self._system_prompt = system_prompt
        
        self._reset_turn_state()

    def start_conversation( self, message_history: list[ChatMessage], user_question: str) -> None:
        self._reset_turn_state()

        initial_message = { "role": "system", "content": self._system_prompt}
        self._running_messages.append(initial_message)

        for message in message_history:
            self._running_messages.append({ "role": message.role, "content": message.content})

        self._running_messages.append({ "role": "user", "content": user_question})

    def _reset_turn_state(self) -> None:
        self._running_messages = []

        self._requested_tool_calls = []
        self._final_answer = None

        self._error_message = None
        self._error_type = None

    def ask_with_tools(self) -> None:
        self._requested_tool_calls = []

        try:
            llm_message = self._llm_service.call_with_tool_list( messages=self._running_messages, tools=self._mcp_tools)
            self._parse_llm_message(llm_message)
        except Exception as exc:
            self._set_error(exc)

    def add_message(self, message: dict) -> None:
        self._running_messages.append(message)

    def add_tool_result( self, tool_call_id: str, tool_name: str, content: str) -> None:
        tool_message =  { "role":"tool", "tool_call_id":tool_call_id, "name":tool_name, "content":content }
        self._running_messages.append(tool_message)

    def get_requested_tool_calls(self) -> list[dict]:
        return self._requested_tool_calls

    def get_final_answer(self) -> str | None:
        return self._final_answer

    def get_error_type(self) -> str | None:
        return self._error_type

    def get_error_message(self) -> str | None:
        return self._error_message

    def _parse_llm_message(self, llm_message: dict) -> None:
        
        tool_calls = llm_message.get("tool_calls") or []

        if tool_calls:
            self._requested_tool_calls = tool_calls
            self._final_answer = None

            # Important: assistant tool-call message must be added
            # before tool results are added.
            self._running_messages.append(llm_message)
            return

        content = llm_message.get("content")

        if content and content.strip():
            self._final_answer = content
            return
        
        self._error_type = "LLMNoAnswerError"
        self._error_message = "LLM returned neither tool calls nor a final answer."

    def _set_error(self, exc: Exception) -> None:
        self._error_type = exc.__class__.__name__
        self._error_message = str(exc)

        self._requested_tool_calls = []