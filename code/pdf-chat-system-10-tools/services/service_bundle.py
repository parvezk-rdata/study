# services/service_bundle.py

from dataclasses import dataclass
from services.pdf.pdf_controller import PDFController
from services.llm.llm_controller import LLMController
from services.mcp.controller import MCPController

@dataclass(frozen=True)
class ServiceBundle:
    pdf: PDFController
    llm: LLMController
    mcp: MCPController