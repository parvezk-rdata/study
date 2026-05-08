
# services/mcp/get_work_directory_tool/controller.py

import json

from services.mcp.clients.client_sync import SyncConnection
from services.mcp.clients.error_types import ErrorType

from services.mcp.get_work_directory_tool.response import (
    GetWorkingDirectoryResponse,
    GetWorkingDirectorySuccessResponse,
    GetWorkingDirectoryErrorResponse,
)


class GetWorkingDirectoryController(SyncConnection):

    TOOL_NAME = "get_working_directory"

    def execute(self) -> GetWorkingDirectoryResponse:

        # Step 1: call tool — no input validation needed
        result = self._run(
            tool_name=self.TOOL_NAME,
            arguments={},
        )

        # Step 2: connection or tool call failed
        if result is None:
            error_type: ErrorType = "ConnectionError" if not self.connected else "ToolCallError"
            error_message = "Server unreachable." if not self.connected else "Tool call failed."
            return GetWorkingDirectoryErrorResponse(
                error_type=error_type,
                error_message=error_message,
            )

        # Step 3: parse MCP result into correct subclass
        try:
            data = json.loads(result.content[0].text)
            if data["success"]:
                return GetWorkingDirectorySuccessResponse.model_validate(data)
            else:
                return GetWorkingDirectoryErrorResponse.model_validate(data)
        except Exception as e:
            return GetWorkingDirectoryErrorResponse(
                error_type="ParseError",
                error_message=str(e),
            )