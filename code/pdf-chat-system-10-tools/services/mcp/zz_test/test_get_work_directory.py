"""
cd  project_root
python -m services.mcp.zz_test.test_get_work_directory
"""

# services/mcp/zz_test/test_get_work_directory.py

from services.mcp.get_work_directory_tool.controller import GetWorkingDirectoryController
from services.mcp.get_work_directory_tool.response import (
    GetWorkingDirectorySuccessResponse,
    GetWorkingDirectoryErrorResponse,
)

SERVER_URL = "http://localhost:8000/mcp"


def print_response(response):
    print(f"success: {response.success}")
    if isinstance(response, GetWorkingDirectorySuccessResponse):
        print(f"directory_path: {response.directory_path}")
    elif isinstance(response, GetWorkingDirectoryErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


def test_success():
    """Server returns working directory — expects success: true."""
    print("\n--- get_working_directory [success] ---")
    controller = GetWorkingDirectoryController(server_url=SERVER_URL)
    response = controller.execute()
    print_response(response)


def test_server_unreachable():
    """Wrong server URL — expects ConnectionError."""
    print("\n--- get_working_directory [server unreachable] ---")
    controller = GetWorkingDirectoryController(server_url="http://localhost:9999/mcp")
    response = controller.execute()
    print_response(response)


if __name__ == "__main__":
    test_success()
    # test_server_unreachable()