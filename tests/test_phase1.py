"""
Phase 1 Validation Tests
Tests core configuration loading, model serialization, and schema validation.
"""
import pytest
from src.core.config import Settings
from src.core.models import (
    Document,
    DocumentChunk,
    Entity,
    EntityType,
    Relationship,
    KnowledgeGraph,
    Citation,
    QueryRequest,
    QueryResponse,
    QueryMode,
)


def test_settings_initialization():
    settings = Settings()
    assert settings.APP_NAME == "GraphRAG-Knowledge-System"
    assert settings.CHUNK_SIZE > 0
    assert settings.CHUNK_OVERLAP >= 0
    assert settings.HYBRID_ALPHA >= 0.0 and settings.HYBRID_ALPHA <= 1.0


def test_document_and_chunk_models():
    doc = Document(filename="attention.pdf", content="Self-attention mechanism details...")
    assert doc.id.startswith("doc_")
    assert doc.filename == "attention.pdf"

    chunk = DocumentChunk(
        document_id=doc.id,
        chunk_index=0,
        content="Self-attention allows positions to attend to all positions.",
        token_count=12,
    )
    assert chunk.id.startswith("chunk_")
    assert chunk.document_id == doc.id
    assert chunk.chunk_index == 0


def test_entity_and_relationship_models():
    e1 = Entity(
        id="transformer",
        name="Transformer Architecture",
        type=EntityType.CONCEPT,
        description="A sequence transduction model based entirely on attention.",
    )
    e2 = Entity(
        id="mha",
        name="Multi-Head Attention",
        type=EntityType.METHOD,
        description="An attention mechanism running k attention functions in parallel.",
    )
    rel = Relationship(
        source_id=e1.id,
        target_id=e2.id,
        relation_type="UTILIZES",
        description="Transformer utilizes multi-head attention for representation learning.",
        weight=0.95,
        evidence_text="Instead of performing a single attention function, we found it beneficial...",
    )

    graph = KnowledgeGraph(nodes=[e1, e2], edges=[rel])
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
    assert graph.edges[0].relation_type == "UTILIZES"
    assert graph.edges[0].weight == 0.95


def test_query_and_citation_models():
    citation = Citation(
        document_id="doc_123",
        chunk_id="chunk_456",
        snippet="Vaswani et al. proposed the Transformer...",
        relevance_score=0.92,
    )
    req = QueryRequest(query="What is Transformer?", mode=QueryMode.HYBRID)
    assert req.mode == QueryMode.HYBRID

    res = QueryResponse(
        query=req.query,
        answer="The Transformer is a neural network architecture...",
        confidence=0.95,
        citations=[citation],
        reasoning_path=[{"source": "Transformer", "relation": "INVENTED_IN", "target": "2017"}],
    )
    assert len(res.citations) == 1
    assert res.citations[0].chunk_id == "chunk_456"
    assert res.confidence == 0.95
