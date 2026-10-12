"""
Configuration settings for GraphRAG Knowledge System.
Loads environment variables with fallback defaults.
"""
from typing import Optional
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # General App Config
    APP_NAME: str = "GraphRAG-Knowledge-System"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"

    # LLM Settings
    LLM_PROVIDER: str = "openai"  # openai | anthropic | local
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.0
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS: int = 1536

    # Neo4j Graph DB Settings
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "graphrag_password"
    NEO4J_DATABASE: str = "neo4j"

    # Qdrant Vector DB Settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "graphrag_chunks"
    QDRANT_API_KEY: Optional[str] = None

    # Ingestion & Chunking
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100
    MAX_EXTRACTION_WORKERS: int = 4

    # Retrieval Settings
    HYBRID_ALPHA: float = 0.5  # 0.0 = only vector, 1.0 = only graph
    TOP_K_CHUNKS: int = 5
    GRAPH_TRAVERSAL_HOPS: int = 2
    MAX_SUBGRAPH_NODES: int = 25


settings = Settings()
