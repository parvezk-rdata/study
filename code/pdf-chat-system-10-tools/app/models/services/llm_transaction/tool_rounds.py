# app/models/services/llm_transaction/tool_rounds.py

from dataclasses import dataclass, field
from typing import Any



@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    tool_call_id: str
    name: str
    arguments: dict[str, Any]
    content: Any
    success: bool = True
    error_message: str | None = None


@dataclass
class ToolRound:
    round_no: int
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_results: list[ToolResult] = field(default_factory=list)