# services/mcp/executor/executor_service.py

from typing import Any
from services.mcp.clients.client_sync import SyncConnection


class MCPExecutorService:
    """
    Raw MCP call only.
    Calls SyncConnection.run() and returns the raw result.
    All error handling is the caller's responsibility.
    """

    def __init__(self, connection: SyncConnection) -> None:
        self._connection = connection

    def execute(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        return self._connection.run(tool_name=tool_name, arguments=arguments)
