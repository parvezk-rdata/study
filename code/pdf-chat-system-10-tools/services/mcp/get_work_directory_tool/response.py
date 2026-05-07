# mcp/get_work_directory_tool/response.py

from typing import Literal
from pydantic import BaseModel

from mcp.clients.error_types import ErrorType


class GetWorkingDirectoryResponse(BaseModel):
    success: bool


class GetWorkingDirectorySuccessResponse(GetWorkingDirectoryResponse):
    success: Literal[True] = True
    directory_path: str


class GetWorkingDirectoryErrorResponse(GetWorkingDirectoryResponse):
    success: Literal[False] = False
    error_type: ErrorType
    error_message: str