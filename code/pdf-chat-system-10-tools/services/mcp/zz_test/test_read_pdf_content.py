
"""
python -m services.mcp.zz_test.test_read_pdf_content
"""

# services/mcp/zz_test/test_read_pdf_content.py

VALID_PDF_PATH = "/media/newuser/data/repos/study/code/mcp-server/ms-03-pdf-text-reader/zz_test/work/test_doc.pdf"
INVALID_PDF_PATH = "/non/existent/file.pdf"
NON_PDF_PATH = "/media/newuser/data/repos/study/code/mcp-server/ms-03-pdf-text-reader/zz_test/work/sample.txt"

from services.mcp.read_pdf_content_tool.controller import ReadPDFContentController
from services.mcp.read_pdf_content_tool.response import (
    ReadPDFContentSuccessResponse,
    ReadPDFContentErrorResponse,
)

SERVER_URL = "http://localhost:8000/mcp"


def print_response(response):
    print(f"success: {response.success}")
    if isinstance(response, ReadPDFContentSuccessResponse):
        print(f"pdf_path  : {response.pdf_path}")
        print(f"page_count: {response.page_count}")
        print(f"full_text : {response.full_text[:200]}..." if len(response.full_text) > 200 else f"full_text : {response.full_text}")
    elif isinstance(response, ReadPDFContentErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


def test_success():
    """Valid PDF path — expects success: true with text and page count."""
    print("\n--- read_pdf_content [success] ---")
    controller = ReadPDFContentController(server_url=SERVER_URL)
    response = controller.execute(pdf_path=VALID_PDF_PATH)
    print_response(response)


def test_pdf_not_found():
    """Non-existent PDF path — expects server-side ValidationError."""
    print("\n--- read_pdf_content [pdf not found] ---")
    controller = ReadPDFContentController(server_url=SERVER_URL)
    response = controller.execute(pdf_path=INVALID_PDF_PATH)
    print_response(response)


def test_non_pdf_file():
    """Non-PDF extension — expects server-side ValidationError."""
    print("\n--- read_pdf_content [non pdf file] ---")
    controller = ReadPDFContentController(server_url=SERVER_URL)
    response = controller.execute(pdf_path=NON_PDF_PATH)
    print_response(response)


def test_empty_path():
    """Empty string — expects client-side ValidationError before network call."""
    print("\n--- read_pdf_content [empty path] ---")
    controller = ReadPDFContentController(server_url=SERVER_URL)
    response = controller.execute(pdf_path="")
    print_response(response)


def test_server_unreachable():
    """Wrong server URL — expects ConnectionError."""
    print("\n--- read_pdf_content [server unreachable] ---")
    controller = ReadPDFContentController(server_url="http://localhost:9999/mcp")
    response = controller.execute(pdf_path=VALID_PDF_PATH)
    print_response(response)


if __name__ == "__main__":
    test_success()
    test_pdf_not_found()
    test_non_pdf_file()
    test_empty_path()
    #test_server_unreachable()