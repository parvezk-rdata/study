# config/embeddings.py

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


    # store_text: bool = False
    # If True, store the original chunk text along with the generated embedding.
    # Useful for debugging, inspection, and later traceability.

    store_metadata: bool = True
    # If True, store chunk and source metadata along with the generated embedding.
    # (e.g., source_id, chunk_id, chunk_path)
    # Useful for filtering, traceability, and Phase 4 vector database storage.

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

    timeout: int = 30
    # Maximum time in seconds to wait for one embedding request.
    # If the request takes longer than this, it is treated as failed.

    retry_attempts: int = 3
    # Number of times to retry a failed embedding request.
    # Useful for handling temporary network or service issues.

    retry_delay: int = 5
    # Time in seconds to wait between retry attempts.
    # Helps avoid immediate repeated failures when the service is temporarily unavailable.