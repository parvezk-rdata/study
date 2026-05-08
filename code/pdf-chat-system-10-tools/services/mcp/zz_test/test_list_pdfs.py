
"""
python -m mcp.zz_test.test_list_pdfs
"""

# python -m services.mcp.zz_test.test_list_pdfs

VALID_DIRECTORY = "/media/newuser/data/repos/study/code/mcp-server/ms-03-pdf-text-reader/zz_test/work"

from services.mcp.list_pdf_tool.controller import ListPDFsController
from services.mcp.list_pdf_tool.response import (
    ListPDFsSuccessResponse,
    ListPDFsErrorResponse,
)

SERVER_URL = "http://localhost:8000/mcp"


def print_response(response):
    print(f"success: {response.success}")
    if isinstance(response, ListPDFsSuccessResponse):
        print(f"directory_path: {response.directory_path}")
        print(f"total_count   : {response.total_count}")
        print(f"pdf_files     : {response.pdf_files}")
    elif isinstance(response, ListPDFsErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


def test_success():
    """Valid directory with PDFs — expects success: true."""
    print("\n--- list_pdfs_in_directory [success] ---")
    controller = ListPDFsController(server_url=SERVER_URL)
    response = controller.execute(directory_path=VALID_DIRECTORY)
    print_response(response)


def test_directory_not_found():
    """Non-existent directory — expects DirectoryNotFound from server."""
    print("\n--- list_pdfs_in_directory [directory not found] ---")
    controller = ListPDFsController(server_url=SERVER_URL)
    response = controller.execute(directory_path="/non/existent/path")
    print_response(response)


def test_empty_path():
    """Empty string — expects client-side ValidationError before network call."""
    print("\n--- list_pdfs_in_directory [empty path] ---")
    controller = ListPDFsController(server_url=SERVER_URL)
    response = controller.execute(directory_path="")
    print_response(response)


def test_server_unreachable():
    """Wrong server URL — expects ConnectionError."""
    print("\n--- list_pdfs_in_directory [server unreachable] ---")
    controller = ListPDFsController(server_url="http://localhost:9999/mcp")
    response = controller.execute(directory_path=VALID_DIRECTORY)
    print_response(response)


if __name__ == "__main__":
    test_success()
    test_directory_not_found()
    test_empty_path()
    #test_server_unreachable()