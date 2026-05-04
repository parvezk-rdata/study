# clients/pdf_reader_mcp_client.py

import asyncio
from typing import Any

from client_02_mcp import MCPConnectionClient

"""
    User-facing client for the PDF Reader MCP server.
    Responsibilities:
    - Hide low-level MCP connection details
    - Call PDF Reader tools
    - Parse structured MCP responses
"""

class PDFReaderMCPClient:
    
    def __init__(self, server_url: str):
        self.server_url = server_url
        self._connection = MCPConnectionClient(server_url)

    """Connect to MCP server and initialize session."""
    async def connect(self) -> None:
        await self._connection.connect()

    """Close MCP session and connection."""
    async def close(self) -> None:
        await self._connection.close()

    def is_connected(self) -> bool:
        """Return True if MCP session is active."""
        return self._connection.is_connected()


    # Extract text from a PDF using the MCP tool.
    async def extract_pdf_text_async(self, pdf_path: str) -> dict[str, Any]:
        raw_result = await self._connection.call_tool(
                                tool_name   =   "extract_pdf_text",
                                arguments   =   { "pdf_path": pdf_path}
                    )
        return self._extract_structured_content(raw_result)


    async def _extract_pdf_text_sync_runner(self, pdf_path: str) -> dict[str, Any]:
        await self.connect()

        try:
            return await self.extract_pdf_text_async(pdf_path)

        finally:
            await self.close()

    # Sync helper for simple scripts.
    def extract_pdf_text(self, pdf_path: str) -> dict[str, Any]:
        return asyncio.run( self._extract_pdf_text_sync_runner(pdf_path))

    # --------------------------
    # Response parsing
    # --------------------------

    def _extract_structured_content(self, raw_result: Any) -> dict[str, Any]:
        """
        Extract structuredContent from MCP CallToolResult.

        Your MCP version uses camelCase:
            raw_result.structuredContent
        """

        structured_content = getattr(raw_result, "structuredContent", None)

        if structured_content is None:
            return {
                "success": False,
                "error_type": "MCPResponseError",
                "error_message": "MCP response does not contain structuredContent.",
            }

        return structured_content