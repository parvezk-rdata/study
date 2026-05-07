# mcp/zz_test/test_get_work_directory.py
"""
python -m mcp.zz_test.test_get_work_directory
"""

from mcp.get_work_directory_tool.controller import GetWorkingDirectoryController
from mcp.get_work_directory_tool.response import (
    GetWorkingDirectorySuccessResponse,
    GetWorkingDirectoryErrorResponse,
)

SERVER_URL = "http://localhost:8000/mcp"


def test_get_working_directory():
    controller = GetWorkingDirectoryController(server_url=SERVER_URL)
    response = controller.execute()

    print("\n--- get_working_directory ---")
    print(f"success: {response.success}")

    if isinstance(response, GetWorkingDirectorySuccessResponse):
        print(f"directory_path: {response.directory_path}")

    elif isinstance(response, GetWorkingDirectoryErrorResponse):
        print(f"error_type   : {response.error_type}")
        print(f"error_message: {response.error_message}")


if __name__ == "__main__":
    test_get_working_directory()