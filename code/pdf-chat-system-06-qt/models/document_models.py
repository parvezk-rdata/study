from dataclasses import dataclass


@dataclass
class DocumentInfo:
    filename: str
    file_hash: str
    text: str
    page_count: int
    used_ocr: bool
    char_count: int
    truncated: bool = False

    @property
    def extraction_method(self) -> str:
        return "OCR" if self.used_ocr else "PyPDF"