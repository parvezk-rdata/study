# config/vectorDB.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


# ===============================
# Phase 4: Vector Database Storage
# ===============================

@dataclass(kw_only=True)
class VectorDBConfig:
    enabled: bool = True
    # Turns Phase 4 vector database storage on or off.

    supported_extensions: tuple[str, ...] = (".json",)
    # File extensions that Phase 4 is allowed to read.
    # In the minimal version, vector records are usually loaded from embedding JSON files.

    provider: Literal["faiss", "chroma", "qdrant", "pinecone", "weaviate", "milvus", "custom"] = "chroma"
    # Vector database provider used to store embeddings.

    collection_name: str = "documents"
    # Name of the target collection, index, or namespace in the vector database.

    distance_metric: Literal["cosine", "dot", "euclidean"] = "cosine"
    # Similarity metric used by the vector database for search.

    batch_size: int = 100
    # Number of embedding records inserted together in one batch.

    store_metadata: bool = True
    # If True, metadata from the embedding file is stored along with the vector record.
    # This is useful for filtering, traceability, and retrieval.

    id_field: str = "chunk_id"
    # Metadata field used as the unique identifier for each vector record.

    create_if_missing: bool = True
    # If True, create the target collection or index if it does not already exist.
    # If False, the phase expects the target collection to already exist.

    overwrite: bool = False
    # If True, allow existing vector records with the same id to be replaced.
    # If False, keep existing records and avoid accidental replacement.

    timeout: int = 30
    # Maximum time in seconds to wait for one vector database request.
    # If the request takes longer than this, it is treated as failed.

    retry_attempts: int = 3
    # Number of times to retry a failed vector database request.
    # Useful for handling temporary network or service issues.

    retry_delay: int = 5
    # Time in seconds to wait between retry attempts.
    # Helps avoid immediate repeated failures when the service is temporarily unavailable.

    db_path: str = "vector_db"

    host: Optional[str] = None
    # If provided, connect to this host for network‑based vector DBs.
    # If None, use embedded/local or default host.

    port: Optional[int] = None
    # If provided, use this TCP port; if None, use the provider’s default.