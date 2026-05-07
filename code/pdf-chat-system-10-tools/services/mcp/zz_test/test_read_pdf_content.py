# mcp/zz_test/test_read_pdf_content.py"
"""
python -m mcp.zz_test.test_read_pdf_content
"""

from mcp.read_pdf_content_tool.controller import ReadPDFContentController
from mcp.read_pdf_content_tool.response import (
    ReadPDFContentSuccessResponse,
    ReadPDFContentErrorResponse,
)

SERVER_URL = "http://localhost:8000/mcp"


def test_read_pdf_success():
    """Test with a valid PDF path."""
    controller = ReadPDFContentController(server_url=SERVER_URL)
    response = controller.execute(pdf_path="~/pdfs/sample.pdf")

    print("\n--- read_pdf_content [valid path] ---")
    print(f"success   : {response.success}")

    if isinstance(response, ReadPDFContentSuccessResponse):
        print(f"pdf_path  : {response.pdf_path}")
        print(f"page_count: {response.page_count}")
        print(f"full_text : {response.full_text[:200]}...")

    elif isinstance(response, ReadPDFContentErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


def test_read_pdf_invalid_path():
    """Test with a non-existent PDF path."""
    controller = ReadPDFContentController(server_url=SERVER_URL)
    response = controller.execute(pdf_path="/non/existent/file.pdf")

    print("\n--- read_pdf_content [invalid path] ---")
    print(f"success: {response.success}")

    if isinstance(response, ReadPDFContentErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


def test_read_pdf_empty_path():
    """Test with empty string — should trigger client-side ValidationError."""
    controller = ReadPDFContentController(server_url=SERVER_URL)
    response = controller.execute(pdf_path="")

    print("\n--- read_pdf_content [empty path] ---")
    print(f"success: {response.success}")

    if isinstance(response, ReadPDFContentErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


def test_read_pdf_non_pdf_file():
    """Test with a non-PDF file extension."""
    controller = ReadPDFContentController(server_url=SERVER_URL)
    response = controller.execute(pdf_path="~/pdfs/sample.txt")

    print("\n--- read_pdf_content [non-pdf file] ---")
    print(f"success: {response.success}")

    if isinstance(response, ReadPDFContentErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


if __name__ == "__main__":
    test_read_pdf_success()
    test_read_pdf_invalid_path()
    test_read_pdf_empty_path()
    test_read_pdf_non_pdf_file()