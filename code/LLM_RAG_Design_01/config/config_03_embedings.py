# config/config.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional


# ============================
# Phase 3: Embedding Generation
# ============================

@dataclass(kw_only=True)
class EmbeddingConfig:
    enabled: bool = True
    # Turns Phase 3 embedding generation on or off.

    input_dir: str = "chunks"
    # Directory that contains chunk files created in Phase 2.

    output_dir: str = "embeddings"
    # Directory where generated embedding files will be stored.

    temp_dir: str = "/tmp/pipeline"
    # Temporary working directory used during embedding generation.
    # Useful for intermediate files, request payloads, or temporary artifacts.

    supported_extensions: tuple[str, ...] = (".txt",)
    # File extensions that Phase 3 is allowed to read.
    # In the minimal version, embeddings are usually generated from chunk text files.

    provider: Literal["openai", "huggingface", "sentence_transformers", "custom"] = "sentence_transformers"
    # Embedding provider used to generate vectors.

    model_name: str = "all-MiniLM-L6-v2"
    # Name of the embedding model used to convert chunk text into vectors.

    dimensions: Optional[int] = None
    # Optional embedding vector dimension.
    # Use None when the dimension is fixed by the selected model.

    batch_size: int = 32
    # Number of chunk files processed together in one embedding batch.

    normalize_vectors: bool = True
    # If True, normalize embedding vectors before storing them.
    # This is often useful for cosine-similarity-based retrieval.

    include_metadata: bool = True
    # If True, include chunk and source metadata in the embedding output.

    output_format: Literal["json", "npy"] = "json"
    # File format used to store generated embedding artifacts.

    embedding_file_prefix: str = "embedding_"
    # Prefix used when naming individual embedding files.
    # Example: embedding_0001.json, embedding_0002.json

    embedding_file_extension: str = ".json"
    # File extension used for each generated embedding file.

    overwrite: bool = False
    # If True, replace existing embedding files with newly generated ones.
    # If False, keep existing output and avoid accidental replacement.