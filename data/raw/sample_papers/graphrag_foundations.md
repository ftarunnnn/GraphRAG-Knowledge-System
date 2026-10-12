# GraphRAG: Unlocking LLM Discovery on Complex Text Corpora

## Abstract
The use of Retrieval-Augmented Generation (RAG) to retrieve relevant information from an external knowledge source has become ubiquitous. However, standard RAG fails when the user query requires multi-hop discovery across connected concepts or corpus-level global summarization. GraphRAG addresses this by extracting an entity-relationship knowledge graph from the source documents, pre-computing community clusters using graph clustering algorithms (such as the Leiden method), and generating hierarchical summaries for each community.

## Core Advantages over Baseline RAG
1. Multi-Hop Relational Reasoning: Graph traversal links entities across documents that would never appear together in standard top-k embedding similarity searches.
2. Global Query Synthesis: By creating summaries at varying levels of community hierarchy, GraphRAG can answer comprehensive questions such as "What are the major themes across all research files?"
3. Provenance and Grounding: Every extracted edge maintains pointer references back to source text chunks, guaranteeing verifiable citations and minimizing hallucination.

## Integration Architecture
GraphRAG integrates knowledge graph databases (such as Neo4j) for relational traversal and vector databases (such as Qdrant) for chunk-level semantic search. A hybrid retrieval engine blends dense embedding ranking with graph neighborhood exploration.
