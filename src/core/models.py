"""
Domain models and Pydantic schemas for the GraphRAG Knowledge System.
"""
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    CONCEPT = "CONCEPT"
    MODEL = "MODEL"
    METHOD = "METHOD"
    ORGANIZATION = "ORGANIZATION"
    PERSON = "PERSON"
    BENCHMARK = "BENCHMARK"
    DATASET = "DATASET"
    TOOL = "TOOL"
    OTHER = "OTHER"


class Document(BaseModel):
    """Raw ingested document representation."""
    id: str = Field(default_factory=lambda: f"doc_{uuid.uuid4().hex[:8]}")
    filename: str
    content: str
    file_type: str = "text"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    content_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentChunk(BaseModel):
    """Segmented chunk from an ingested document."""
    id: str = Field(default_factory=lambda: f"chunk_{uuid.uuid4().hex[:8]}")
    document_id: str
    chunk_index: int
    content: str
    token_count: int = 0
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Entity(BaseModel):
    """Knowledge Graph node representing an entity."""
    id: str
    name: str
    type: EntityType = EntityType.CONCEPT
    description: str = ""
    aliases: List[str] = Field(default_factory=list)
    source_chunk_ids: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Relationship(BaseModel):
    """Knowledge Graph directed edge between two entities."""
    id: str = Field(default_factory=lambda: f"rel_{uuid.uuid4().hex[:8]}")
    source_id: str
    target_id: str
    relation_type: str
    description: str = ""
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    source_chunk_id: Optional[str] = None
    evidence_text: str = ""


class KnowledgeGraph(BaseModel):
    """Container for in-memory or exported graph representation."""
    nodes: List[Entity] = Field(default_factory=list)
    edges: List[Relationship] = Field(default_factory=list)


class Citation(BaseModel):
    """Attribution citation linking an answer directly to a source passage."""
    document_id: str
    chunk_id: str
    filename: Optional[str] = None
    snippet: str
    relevance_score: float = 1.0


class QueryMode(str, Enum):
    HYBRID = "hybrid"
    VECTOR_ONLY = "vector_only"
    GRAPH_ONLY = "graph_only"
    GLOBAL = "global"


class QueryRequest(BaseModel):
    """API request model for querying the GraphRAG system."""
    query: str
    mode: QueryMode = QueryMode.HYBRID
    top_k_chunks: int = 5
    graph_hops: int = 2


class QueryResponse(BaseModel):
    """API response model containing synthesized answer and supporting citations."""
    query: str
    answer: str
    confidence: float = 1.0
    citations: List[Citation] = Field(default_factory=list)
    reasoning_path: List[Dict[str, Any]] = Field(default_factory=list)
    is_uncertain: bool = False
    execution_time_ms: float = 0.0


class Community(BaseModel):
    """Cluster of closely connected entities detected in Phase 7."""
    id: int
    title: str
    summary: str
    level: int = 0
    entity_ids: List[str] = Field(default_factory=list)
