# services/llm/formatters/base_tool_formatter.py

from abc import ABC, abstractmethod

from services.mcp.models.tool_definition import ToolDefinition


class BaseToolFormatter(ABC):
    """
    Base class for converting neutral ToolDefinition models
    into LLM-specific tool schemas.
    """

    @abstractmethod
    def format_tools(self, tools: list[ToolDefinition]) -> list[dict]:
        pass