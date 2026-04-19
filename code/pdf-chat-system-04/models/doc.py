from __future__ import annotations

from pydantic import BaseModel


class ExtractedDoc(BaseModel):
    """Represents a PDF document after text extraction."""
    text: str
    page_count: int
    used_ocr: bool

    @property
    def char_count(self) -> int:
        return len(self.text)
