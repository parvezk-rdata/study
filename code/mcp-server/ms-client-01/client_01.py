import asyncio

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as streams:
        read_stream, write_stream, _ = streams

        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "extract_pdf_text",
                {
                    "pdf_path": "/media/newuser/data/repos/study/code/mcp-server/ms-03-pdf-text-reader/zz_test/test_doc.pdf"
                },
            )

            print(result.structuredContent)


asyncio.run(main())