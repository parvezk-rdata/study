

@dataclass
class ProjectPaths:
    project_root: str = "."
    # Root directory of the project.
    # All other paths are relative to this unless explicitly absolute.

    raw_dir: str = "raw"
    # Directory that contains raw input files.

    normalized_dir: str = "normalized"
    # Directory that contains normalized text files.

    chunk_dir: str = "chunks"
    # Directory that contains chunk files.

    embedding_dir: str = "embeddings"
    # Directory that contains embedding files.

    vector_db_dir: str = "vector_db"
    # Directory (or base path) for the vector database index / collections.

    temp_dir: str = "/tmp/pipeline"
    # Temporary directory used during processing.
    # Useful for intermediate artifacts, transient files, and scratch space.


@dataclass
class ProjectConfig:
    enabled_normalization:  bool = True
    enabled_chunking:       bool = True
    enabled_embedding:      bool = True
    enabled_vector_db:      bool = True