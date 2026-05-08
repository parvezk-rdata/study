# app/models/transformers/base_formatter.py

from abc import ABC, abstractmethod

from app.models.services.llm_transaction.chat_message import ChatMessage
from app.models.services.llm_transaction.mcp_tool_definition import MCPToolDefinition
from app.models.services.llm_transaction.tool_rounds import ToolCall, ToolResult, ToolRound
from app.models.services.llm_transaction.llm_transaction import LLMTransaction


class BaseLLMFormatter(ABC):

    @abstractmethod
    def format_message(self, message: ChatMessage) -> dict: ...

    @abstractmethod
    def format_tool_definition(self, tool: MCPToolDefinition) -> dict: ...

    @abstractmethod
    def format_tool_call(self, tool_call: ToolCall) -> dict: ...

    @abstractmethod
    def format_tool_result(self, tool_result: ToolResult) -> dict: ...

    @abstractmethod
    def format_tool_round(self, tool_round: ToolRound) -> list[dict]: ...

    def build_messages(self, transaction: LLMTransaction) -> list[dict]:
        messages = []
        messages += [self.format_message(m) for m in transaction.history]
        messages.append(self.format_message(transaction.user_message))
        for tool_round in transaction.tool_rounds:
            messages += self.format_tool_round(tool_round)
        return messages

    def build_tools(self, transaction: LLMTransaction) -> list[dict]:
        return [self.format_tool_definition(t) for t in transaction.available_tools]