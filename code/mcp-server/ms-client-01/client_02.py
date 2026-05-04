from typing import Any

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPConnectionClient:
    """
    General-purpose MCP client to -
    - Manage connection lifecycle
    - Maintain persistent session
    - Call MCP tools
    """

    def __init__(self, server_url: str):
        self.server_url = server_url

        # Internal state
        self._streams_ctx = None
        self._streams = None
        self._session: ClientSession | None = None

    # Create connection and initialize session.
    async def connect(self) -> None:
        if self._session is not None:
            return  # already connected

        # Create stream context
        self._streams_ctx = streamablehttp_client(self.server_url)
        self._streams = await self._streams_ctx.__aenter__()

        read_stream, write_stream, _ = self._streams

        # Create session
        self._session = ClientSession(read_stream, write_stream)
        await self._session.__aenter__()

        # Initialize session
        await self._session.initialize()

    # Close session and connection.
    async def close(self) -> None:
        if self._session is not None:
            await self._session.__aexit__(None, None, None)
            self._session = None

        if self._streams_ctx is not None:
            await self._streams_ctx.__aexit__(None, None, None)
            self._streams_ctx = None
            self._streams = None

    # Check if client is connected.
    def is_connected(self) -> bool:
        return self._session is not None

    # Call MCP tool using existing session.
    async def call_tool( self, tool_name: str, arguments: dict[str, Any]) -> Any:
        if self._session is None: return None
        return await self._session.call_tool( tool_name, arguments )