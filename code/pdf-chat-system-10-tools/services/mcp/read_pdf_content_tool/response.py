# mcp/read_pdf_content_tool/response.py

from typing import Literal
from pydantic import BaseModel

from mcp.clients.error_types import ErrorType


class ReadPDFContentResponse(BaseModel):
    success: bool


class ReadPDFContentSuccessResponse(ReadPDFContentResponse):
    success: Literal[True] = True
    pdf_path: str
    full_text: str
    page_count: int


class ReadPDFContentErrorResponse(ReadPDFContentResponse):
    success: Literal[False] = False
    error_type: ErrorType
    error_message: str