# mcp/zz_test/test_list_pdfs.py
"""
python -m mcp.zz_test.test_list_pdfs
"""

from mcp.list_pdf_tool.controller import ListPDFsController
from mcp.list_pdf_tool.response import (
    ListPDFsSuccessResponse,
    ListPDFsErrorResponse,
)

SERVER_URL = "http://localhost:8000/mcp"


def test_list_pdfs_success():
    """Test with a valid directory path."""
    controller = ListPDFsController(server_url=SERVER_URL)
    response = controller.execute(directory_path="~/pdfs")

    print("\n--- list_pdfs_in_directory [valid path] ---")
    print(f"success: {response.success}")

    if isinstance(response, ListPDFsSuccessResponse):
        print(f"directory_path: {response.directory_path}")
        print(f"total_count   : {response.total_count}")
        print(f"pdf_files     : {response.pdf_files}")

    elif isinstance(response, ListPDFsErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


def test_list_pdfs_invalid_path():
    """Test with a non-existent directory path."""
    controller = ListPDFsController(server_url=SERVER_URL)
    response = controller.execute(directory_path="/non/existent/path")

    print("\n--- list_pdfs_in_directory [invalid path] ---")
    print(f"success: {response.success}")

    if isinstance(response, ListPDFsSuccessResponse):
        print(f"directory_path: {response.directory_path}")
        print(f"total_count   : {response.total_count}")
        print(f"pdf_files     : {response.pdf_files}")

    elif isinstance(response, ListPDFsErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


def test_list_pdfs_empty_path():
    """Test with empty string — should trigger client-side ValidationError."""
    controller = ListPDFsController(server_url=SERVER_URL)
    response = controller.execute(directory_path="")

    print("\n--- list_pdfs_in_directory [empty path] ---")
    print(f"success: {response.success}")

    if isinstance(response, ListPDFsErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


if __name__ == "__main__":
    test_list_pdfs_success()
    test_list_pdfs_invalid_path()
    test_list_pdfs_empty_path()