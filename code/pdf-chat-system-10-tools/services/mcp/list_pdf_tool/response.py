# list_pdf_tool/response.py

from typing import Literal
from pydantic import BaseModel

from mcp_connection.error_types import ErrorType


class ListPDFsResponse(BaseModel):
    success: bool


class ListPDFsSuccessResponse(ListPDFsResponse):
    success: Literal[True] = True
    directory_path: str
    pdf_files: list[str]
    total_count: int


class ListPDFsErrorResponse(ListPDFsResponse):
    success: Literal[False] = False
    error_type: ErrorType
    error_message: str