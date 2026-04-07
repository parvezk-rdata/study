
# ================================
# Phase 1: Normalized File Creation
# ================================

# config/config.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional



@dataclass(kw_only=True)
class NormalizationConfig:
    enabled: bool = True
    # Turns Phase 1 normalization on or off.

    input_dir: str = "raw"
    # Directory that contains the raw input files to be normalized.

    output_dir: str = "normalized"
    # Directory where normalized text files will be written.

    temp_dir: str = "/tmp/pipeline"
    # Temporary working directory used during normalization.
    # Useful for intermediate files, extracted text, or temporary processing.

    supported_extensions: tuple[str, ...] = (".txt", ".md", ".html", ".pdf", ".docx")
    # File extensions that Phase 1 is allowed to process.
    # Files with other extensions can be skipped or rejected.

    output_extension: str = ".txt"
    # File extension for the normalized output file.

    input_encoding: str = "utf-8"
    # Expected encoding when reading the raw input file.

    encoding_errors: Literal["strict", "ignore", "replace"] = "replace"
    # What to do if file decoding fails:
    # - "strict"  -> raise an error
    # - "ignore"  -> skip bad characters
    # - "replace" -> replace bad characters with a placeholder

    min_chars: int = 1
    # Minimum number of characters required after normalization.
    # Files with fewer characters can be rejected as too small or empty.

    max_chars: Optional[int] = None
    # Optional upper limit on character count after normalization.
    # Use None to allow any size.

    normalize_unicode: Literal["NFC", "NFKC", "NFD", "NFKD"] = "NFC"
    # Unicode normalization strategy used to standardize text representation.

    normalize_unicode_data: bool = True

    trim_whitespace: bool = True
    # Removes leading and trailing whitespace from the final normalized text.

    preserve_paragraphs: bool = True
    # Keeps paragraph boundaries and newlines instead of flattening all text
    # into a single block.

    remove_empty_lines: bool = True
    # Removes blank lines from the normalized text.
    # Useful for making output cleaner and more consistent.

    overwrite: bool = False
    # If True, replace an existing normalized file with the new one.
    # If False, keep existing output and avoid accidental replacement.