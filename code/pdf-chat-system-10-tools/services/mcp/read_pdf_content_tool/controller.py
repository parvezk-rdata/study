# mcp/read_pdf_content_tool/controller.py

from pydantic import ValidationError

from mcp.clients.base_controller import SyncConnection
from mcp.clients.error_types import ErrorType

from mcp.read_pdf_content_tool.request import ReadPDFContentRequest
from mcp.read_pdf_content_tool.response import (
    ReadPDFContentResponse,
    ReadPDFContentErrorResponse,
)


class ReadPDFContentController(SyncConnection):

    TOOL_NAME = "read_pdf_content"

    def execute(self, pdf_path: str) -> ReadPDFContentResponse:

        # Step 1: validate input
        try:
            request = ReadPDFContentRequest(pdf_path=pdf_path)
        except ValidationError as e:
            return ReadPDFContentErrorResponse(
                error_type="ValidationError",
                error_message=str(e),
            )

        # Step 2: call tool
        result = self._run(
            tool_name=self.TOOL_NAME,
            arguments={"pdf_path": request.pdf_path},
        )

        # Step 3: connection or tool call failed
        if result is None:
            error_type: ErrorType = "ConnectionError" if not self.connected else "ToolCallError"
            error_message = "Server unreachable." if not self.connected else "Tool call failed."
            return ReadPDFContentErrorResponse(
                error_type=error_type,
                error_message=error_message,
            )

        # Step 4: parse MCP result into response model
        try:
            content = result.content[0].text
            return ReadPDFContentResponse.model_validate_json(content)
        except Exception as e:
            return ReadPDFContentErrorResponse(
                error_type="ParseError",
                error_message=str(e),
            )