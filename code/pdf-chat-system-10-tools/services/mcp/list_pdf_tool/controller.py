
# services/mcp/list_pdf_tool/controller.py

import json

from pydantic import ValidationError

from services.mcp.clients.client_sync import SyncConnection
from services.mcp.clients.error_types import ErrorType

from services.mcp.list_pdf_tool.request import ListPDFsRequest
from services.mcp.list_pdf_tool.response import (
    ListPDFsResponse,
    ListPDFsSuccessResponse,
    ListPDFsErrorResponse,
)


class ListPDFsController(SyncConnection):

    TOOL_NAME = "list_pdfs_in_directory"

    def execute(self, directory_path: str) -> ListPDFsResponse:

        # Step 1: validate input
        try:
            request = ListPDFsRequest(directory_path=directory_path)
        except ValidationError as e:
            return ListPDFsErrorResponse(
                error_type="ValidationError",
                error_message=str(e),
            )

        # Step 2: call tool
        result = self._run(
            tool_name=self.TOOL_NAME,
            arguments={"directory_path": request.directory_path},
        )

        # Step 3: connection or tool call failed
        if result is None:
            error_type: ErrorType = "ConnectionError" if not self.connected else "ToolCallError"
            error_message = "Server unreachable." if not self.connected else "Tool call failed."
            return ListPDFsErrorResponse(
                error_type=error_type,
                error_message=error_message,
            )

        # Step 4: parse MCP result into correct subclass
        try:
            data = json.loads(result.content[0].text)
            if data["success"]:
                return ListPDFsSuccessResponse.model_validate(data)
            else:
                return ListPDFsErrorResponse.model_validate(data)
        except Exception as e:
            return ListPDFsErrorResponse(
                error_type="ParseError",
                error_message=str(e),
            )