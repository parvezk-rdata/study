# services/llm/formatters/openai_tool_formatter.py

from services.llm.formatters.base_tool_formatter import BaseToolFormatter
from services.mcp.models.mcp_tool_definition import ToolDefinition, ToolParameter


class OpenAIToolFormatter(BaseToolFormatter):
    """
    Converts neutral ToolDefinition models into OpenAI tool schema.
    """

    def format_tools(self, tools: list[ToolDefinition]) -> list[dict]:
        return [self._format_single_tool(tool) for tool in tools]

    def _format_single_tool(self, tool: ToolDefinition) -> dict:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": self._build_parameters_schema(tool.parameters),
            },
        }

    def _build_parameters_schema(self, parameters: list[ToolParameter]) -> dict:
        properties: dict = {}
        required: list[str] = []

        for param in parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description,
            }

            if param.required:
                required.append(param.name)

        schema = {
            "type": "object",
            "properties": properties,
            "additionalProperties": False,
        }

        if required:
            schema["required"] = required

        return schema