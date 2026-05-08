# app/models/transformers/openai_formatter.py

import json

from app.models.services.llm_transaction.chat_message import ChatMessage
from app.models.services.llm_transaction.mcp_tool_definition import MCPToolDefinition
from app.models.services.llm_transaction.tool_rounds import ToolCall, ToolResult, ToolRound

from app.models.transformers.base_formatter import BaseLLMFormatter


class OpenAIFormatter(BaseLLMFormatter):

    def format_message(self, message: ChatMessage) -> dict:
        return {
            "role": message.role,
            "content": message.content,
        }

    def format_tool_definition(self, tool: MCPToolDefinition) -> dict:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        p.name: {
                            "type": p.type,
                            "description": p.description,
                        }
                        for p in tool.parameters
                    },
                    "required": [
                        p.name for p in tool.parameters if p.required
                    ],
                },
            },
        }

    def format_tool_call(self, tool_call: ToolCall) -> dict:
        return {
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.name,
                "arguments": json.dumps(tool_call.arguments),
            },
        }

    def format_tool_result(self, tool_result: ToolResult) -> dict:
        content = tool_result.model_dump(
            exclude={"tool_call_id", "name", "arguments"}
        )
        return {
            "role": "tool",
            "tool_call_id": tool_result.tool_call_id,
            "name": tool_result.name,
            "content": json.dumps(content),
        }

    def format_tool_round(self, tool_round: ToolRound) -> list[dict]:
        messages = []

        messages.append({
            "role": "assistant",
            "tool_calls": [
                self.format_tool_call(tc) for tc in tool_round.tool_calls
            ],
        })

        for tool_result in tool_round.tool_results:
            messages.append(self.format_tool_result(tool_result))

        return messages