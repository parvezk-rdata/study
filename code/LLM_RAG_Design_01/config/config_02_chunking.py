# config/config.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

# there are various chunking stratgies and for each there are parameters

# =======================
# Phase 2: Chunk Creation
# =======================

@dataclass(kw_only=True)
class ChunkingConfig:
    enabled: bool = True
    # Turns Phase 2 chunk creation on or off.

    input_dir: str = "normalized"
    # Directory that contains normalized text files created in Phase 1.

    output_dir: str = "chunks"
    # Directory where generated chunk files will be stored.

    temp_dir: str = "/tmp/pipeline"
    # Temporary working directory used during chunk creation.
    # Useful for intermediate processing or temporary chunk artifacts.

    supported_extensions: tuple[str, ...] = (".txt",)
    # File extensions that Phase 2 is allowed to read.
    # In the minimal version, chunking usually starts from normalized text files.

    chunk_size: int = 1000
    # Target maximum size of each chunk.

    chunk_overlap: int = 100
    # Amount of overlap between consecutive chunks.
    # Overlap helps preserve context across chunk boundaries.

    chunk_unit: Literal["characters", "tokens", "sentences"] = "characters"
    # Unit used to measure chunk_size, chunk_overlap, and min_chunk_size.

    min_chunk_size: int = 200
    # Minimum allowed size for a chunk.
    # Chunks smaller than this threshold can be filtered out or merged with neighbors.

    merge_small_chunks: bool = True
    # If True, small chunks below min_chunk_size are merged with adjacent chunks.
    # If False, small chunks are kept as-is or dropped based on pipeline policy.

    chunking_strategy: Literal["fixed", "recursive"] = "recursive"
    # Strategy used to split normalized text into chunks.
    # - "fixed"     -> split strictly by size
    # - "recursive" -> try larger separators first, then smaller ones

    separators: tuple[str, ...] = ("\n\n", "\n", ". ", " ")
    # Ordered separators used when splitting text recursively.
    # The splitter tries earlier separators first to preserve structure.

    chunk_file_prefix: str = "chunk_"
    # Prefix used when naming individual chunk files.
    # Example: chunk_0001.txt, chunk_0002.txt

    chunk_file_extension: str = ".txt"
    # File extension used for each generated chunk file.

    overwrite: bool = False
    # If True, replace existing chunk files with newly generated ones.
    # If False, keep existing output and avoid accidental replacement.