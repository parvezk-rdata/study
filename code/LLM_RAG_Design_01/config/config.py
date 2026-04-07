# config/config.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional


# 1. Chunking-related settings
@dataclass
class ChunkingConfig:
    chunk_size: int = 500
    chunk_overlap: int = 50
    splitter_type: Literal["fixed", "recursive"] = "recursive"


# 2. Prompt-related settings
@dataclass
class PromptConfig:
    system_prompt: str = (
        "You are a helpful assistant. "
        "Answer the question strictly using the provided context. "
        "If the answer is not present in the context, say you do not know."
    )
    include_sources: bool = True
    max_context_chunks: int = 4


# 3. Embedding-related settings
@dataclass
class EmbeddingConfig:
    provider: Literal["openai"] = "openai"
    model_name: str = "text-embedding-3-small"


# 4. Vector store settings
@dataclass
class VectorStoreConfig:
    backend: Literal["chroma", "faiss", "sqlite"] = "faiss"
    persist_path: str = "data/vector_store"
    collection_name: str = "rag_documents"


# 5. LLM-related settings
@dataclass
class LLMConfig:
    provider: Literal["openai"] = "openai"
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.0
    max_tokens: int = 512


# 6. Ingestion-related settings
@dataclass
class IngestionConfig:
    supported_file_types: tuple[str, ...] = (".pdf", ".txt", ".md")
    encoding: str = "utf-8"


# 7. Top-level application config
@dataclass
class AppConfig:
    chunking: ChunkingConfig = ChunkingConfig()
    prompt: PromptConfig = PromptConfig()
    embedding: EmbeddingConfig = EmbeddingConfig()
    vector_store: VectorStoreConfig = VectorStoreConfig()
    llm: LLMConfig = LLMConfig()
    ingestion: IngestionConfig = IngestionConfig()
