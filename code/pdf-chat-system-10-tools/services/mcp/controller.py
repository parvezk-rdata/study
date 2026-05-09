# services/mcp/mcp_tool_controller.py

import json
from typing import Any

from services.mcp.clients.sync_connection import SyncConnection


class MCPToolController:
    """
    Generic controller for all MCP tool calls.

    Receives a tool name and arguments, delegates to SyncConnection,
    and always returns a plain dict — either the parsed MCP response
    or a structured error dict — ready to be sent to OpenAI as a
    tool_call result. Never raises exceptions.
    """

    def __init__(self, connection: SyncConnection) -> None:
        self._connection = connection

    def call(self, tool_name: str, arguments: dict[str, Any]) -> dict:
        result = self._connection._run(tool_name=tool_name, arguments=arguments)

        if result is None:
            return self._resolve_error()

        return self._parse(result)

    # ------------------------------------------------------------------
    # private
    # ------------------------------------------------------------------

    def _resolve_error(self) -> dict:
        """
        Use SyncConnection state flags to identify exactly where the
        call failed. All three cases are mutually exclusive.
        """
        if not self._connection.connected:
            return {
                "success": False,
                "error_type": "ConnectionError",
                "error_message": "MCP server is not reachable",
            }

        if not self._connection.tool_called:
            return {
                "success": False,
                "error_type": "ToolExecutionError",
                "error_message": "Connected to MCP server but tool execution failed",
            }

        # connected=True, tool_called=True, result is still None
        return {
            "success": False,
            "error_type": "EmptyResultError",
            "error_message": "Tool was called but returned no content",
        }

    def _parse(self, result: Any) -> dict:
        """
        Extract text from the first content block and parse it as JSON.
        MCP always returns a CallToolResult with content[0].text as a
        JSON string, so this is sufficient for all tools.
        """
        isIndexError = True
        try:
            text = result.content[0].text
            isIndexError = False
            return json.loads(text)
        except Exception as e:
            if isIndexError :
                return {
                    "success": False,
                    "error_type": "ParseError",
                    "error_message": "MCP response contained no content blocks",
                }
            else:
                return {
                    "success": False,
                    "error_type": "ParseError",
                    "error_message": "MCP response content was not valid JSON",
                }