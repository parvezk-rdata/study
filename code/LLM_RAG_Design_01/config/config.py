# config/config.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional


# 1. Chunking-related settings
@dataclass
class ChunkingConfig:
    chunk_size: int = 512                 # characters or tokens
    chunk_overlap: int = 64
    unit: Literal["tokens", "characters"] = "tokens"
    strategy: Literal["fixed", "recursive", "by_title"] = "fixed"
    max_chunks: Optional[int] = None      # optional global cap
    respect_sentence_boundary: bool = False


# 2. Prompt-related settings
@dataclass
class PromptConfig:
    system_prompt: str = (
        "You are a helpful assistant that answers using the provided context."
    )
    max_context_chunks: int = 4
    include_metadata: bool = True
    # optional: allow easy switch to different prompt styles later
    template_name: str = "default"        # or Literal[...] later


# 3. Vector store settings
@dataclass
class VectorStoreConfig:
    backend: Literal["chroma", "faiss", "sqlite"] = "chroma"
    persist_path: str = "data/vector_store"
    collection_name: str = "default"
    top_k: int = 5
    # optional: dimension can be verified against embedding config later
    embedding_dim: Optional[int] = None
