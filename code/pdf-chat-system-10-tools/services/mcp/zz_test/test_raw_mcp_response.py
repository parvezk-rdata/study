"""
python -m services.mcp.zz_test.test_raw_mcp_response

"""

# services/mcp/zz_test/test_read_pdf_content.py

import asyncio
from services.mcp.clients.client_sync import MCPConnectionClient

SERVER_URL = "http://localhost:8000/mcp"
VALID_PDF_PATH = "/media/newuser/data/repos/study/code/mcp-server/ms-03-pdf-text-reader/zz_test/work/test_doc.pdf"
INVALID_PDF_PATH = "/non/existent/file.pdf"
NON_PDF_PATH = "~/pdfs/sample.txt"


async def _inspect(tool_name: str, arguments: dict):
    async with MCPConnectionClient(server_url=SERVER_URL) as client:
        result = await client.call_tool(tool_name, arguments)

        print(f"\n{'='*50}")
        print(f"TOOL: {tool_name}")
        print(f"ARGS: {arguments}")
        print(f"{'='*50}")
        print(f"type(result)          : {type(result)}")
        print(f"type(result.content)  : {type(result.content)}")
        print(f"len(result.content)   : {len(result.content)}")

        for i, block in enumerate(result.content):
            print(f"\n  content[{i}]")
            print(f"  type(block)         : {type(block)}")
            print(f"  block.type          : {block.type}")
            print(f"  block.text          : {block.text[:300]}..." if len(block.text) > 300 else f"  block.text          : {block.text}")


def main():
    # get_working_directory
    asyncio.run(_inspect("get_working_directory", {}))

    # list_pdfs_in_directory — valid path
    asyncio.run(_inspect("list_pdfs_in_directory", {"directory_path": "~/pdfs"}))

    # list_pdfs_in_directory — invalid path
    asyncio.run(_inspect("list_pdfs_in_directory", {"directory_path": "/non/existent"}))

    # read_pdf_content — valid pdf
    asyncio.run(_inspect("read_pdf_content", {"pdf_path": VALID_PDF_PATH}))

    # read_pdf_content — invalid path
    asyncio.run(_inspect("read_pdf_content", {"pdf_path": INVALID_PDF_PATH}))

    # read_pdf_content — non pdf file
    asyncio.run(_inspect("read_pdf_content", {"pdf_path": NON_PDF_PATH}))

    # read_pdf_content — empty path
    asyncio.run(_inspect("read_pdf_content", {"pdf_path": ""}))


if __name__ == "__main__":
    main()