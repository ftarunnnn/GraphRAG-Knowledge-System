# GraphRAG Knowledge System — API Specification

The GraphRAG backend exposes a REST API via FastAPI for ingestion, querying, graph inspection, and analytics.

---

## 1. System Endpoints

### `GET /health`
Returns the operational status of the service and connected storage engines.
- **Response**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "neo4j_connected": true,
  "qdrant_connected": true
}
```

---

## 2. Ingestion Endpoints

### `POST /api/v1/documents/upload`
Uploads raw documents (PDF, Markdown, TXT), processes chunks, and returns an ingestion job summary.
- **Content-Type**: `multipart/form-data`
- **Request Body**: `files: List[UploadFile]`
- **Response**:
```json
{
  "document_id": "doc_8f1a23b9",
  "filename": "attention_is_all_you_need.pdf",
  "total_chunks": 24,
  "status": "processed",
  "created_at": "2026-10-12T16:30:00Z"
}
```

### `GET /api/v1/documents`
Lists all ingested documents with metadata and chunk counts.

---

## 3. Query & GraphRAG Endpoints

### `POST /api/v1/query/answer`
Executes GraphRAG question answering pipeline using hybrid retrieval and multi-hop reasoning.
- **Request Body**:
```json
{
  "query": "How does FlashAttention optimize the memory footprint of Multi-Head Attention?",
  "mode": "hybrid", 
  "top_k_chunks": 5,
  "graph_hops": 2
}
```
- **Response**:
```json
{
  "answer": "FlashAttention reduces the memory footprint by computing exact attention with tiling and kernel fusion...",
  "confidence": 0.94,
  "citations": [
    {
      "document_id": "doc_8f1a23b9",
      "chunk_id": "chunk_04",
      "snippet": "FlashAttention computes exact attention while drastically reducing HBM accesses...",
      "score": 0.91
    }
  ],
  "reasoning_path": [
    { "source": "Multi-Head Attention", "relation": "EXTENDED_BY", "target": "FlashAttention" },
    { "source": "FlashAttention", "relation": "OPTIMIZES", "target": "GPU High Bandwidth Memory" }
  ]
}
```

---

## 4. Knowledge Graph Inspection Endpoints

### `GET /api/v1/graph/subgraph`
Fetches a visual subgraph centered on an entity or seed keywords.
- **Query Parameters**: `entity_name=string`, `hops=int`
- **Response**:
```json
{
  "nodes": [
    { "id": "transformer", "label": "Transformer", "type": "CONCEPT" },
    { "id": "attention", "label": "Self-Attention", "type": "METHOD" }
  ],
  "edges": [
    { "source": "transformer", "target": "attention", "relation": "UTILIZES", "weight": 0.95 }
  ]
}
```

---

## 5. Analytics & Communities Endpoints

### `GET /api/v1/analytics/communities`
Returns detected graph communities and their high-level summaries generated during Phase 7.
- **Response**:
```json
{
  "communities": [
    {
      "community_id": 1,
      "title": "Attention Optimization Techniques",
      "summary": "This cluster groups mechanisms reducing the quadratic memory complexity of attention...",
      "key_entities": ["FlashAttention", "Sparse Attention", "Linear Attention"]
    }
  ]
}
```
