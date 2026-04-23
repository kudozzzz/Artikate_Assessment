# DESIGN.md — Section 2 RAG Pipeline Architecture

## Overview

This section implements a local Retrieval Augmented Generation (RAG) pipeline for querying legal contracts and policy PDFs. The objective is to answer precise document questions with source citations while minimizing hallucinated responses.

The implemented pipeline flow is:

Document Ingestion → Chunking → Embedding → Vector Index → Retrieval → Grounded Answer Generation

---

## 1. Chunking Strategy

### Chosen Approach

- page-aware text extraction from PDFs
- fixed-size overlapping character chunks
- chunk size: 512 characters
- overlap: 100 characters

### Why

Legal documents often contain clauses that span multiple sentences or continue across paragraph boundaries. Using overlap reduces the chance that important language is split between chunks.

Keeping chunks page-aware preserves citation quality because each retrieved chunk can be mapped directly to:

- source file
- page number
- chunk text

### Trade-off

Smaller chunks improve precision but may lose surrounding context. Larger chunks preserve context but reduce retrieval granularity. The selected size balances both.

---

## 2. Embedding Model Choice

### Chosen Model

`BAAI/bge-small-en-v1.5`

### Why

- strong semantic retrieval performance for English text
- lightweight enough for local CPU execution
- faster indexing than larger transformer embeddings
- low setup overhead for a take-home assessment

### Trade-off

Larger embedding models may improve recall slightly, but would increase indexing time and memory use without clear benefit for a small demo corpus.

---

## 3. Vector Store Choice

### Chosen Store

FAISS

### Why FAISS

- fast similarity search
- lightweight local dependency
- no external infrastructure required
- easy persistence to disk
- widely used in retrieval systems

### Why Not Chroma

Chroma is convenient for rapid prototyping but introduces extra abstraction not required for this small local implementation.

### Why Not Pinecone

Pinecone is useful for production managed search but unnecessary here because this assessment runs locally.

---

## 4. Retrieval Strategy

### Implemented Strategy

- embed user query
- search top-k nearest vectors in FAISS
- return highest scoring chunks with metadata

### Why

For a moderate local corpus, dense top-k retrieval is simple, reliable, and fast enough.

### Trade-off

Dense retrieval can miss exact keyword-heavy clauses or numeric language. Hybrid retrieval would improve robustness.

### Future Upgrades

- BM25 + dense hybrid retrieval
- metadata filtering by vendor / contract type
- cross-encoder reranking
- query expansion for legal terminology

---

## 5. Hallucination Mitigation Strategy

### Implemented Controls

- confidence scoring from retrieval similarity
- source-grounded answers using retrieved chunks only
- refusal response when relevant context is insufficient

### Why

Legal question answering requires factual precision. If evidence is weak, refusal is safer than speculative output.

### Trade-off

A conservative refusal threshold may reject some answerable queries, but this is preferable to hallucinated legal advice.

---

## 6. Evaluation Harness

### Method

Created 10 manual question-answer pairs based on the sample PDFs.

Measured:

- Precision@3

Definition:

How often the correct supporting chunk appears in the top three retrieved results.

### Observed Result

- Precision@3 = 1.00 (10/10)

### Limitation

The sample corpus is small and controlled. Real production performance would require larger and more varied legal documents.

---

## 7. Scaling to 50,000 Documents

As corpus size grows, several components become bottlenecks.

### A. Embedding / Ingestion Time

Problem:

Large document batches slow indexing.

Fix:

- parallel embedding jobs
- incremental indexing
- background ingestion workers

### B. Search Performance

Problem:

Exact nearest-neighbor search becomes slower.

Fix:

- IVF indexes
- HNSW indexes
- approximate nearest neighbor search

### C. Metadata Storage

Problem:

Flat local metadata files become harder to manage.

Fix:

- PostgreSQL
- SQLite for smaller deployments

### D. Query Throughput

Problem:

Multiple concurrent users increase latency.

Fix:

- stateless API service
- model warm loading
- request queueing
- caching frequent queries

### E. Retrieval Quality

Problem:

More documents create more near-matches.

Fix:

- reranking stage
- metadata filters
- hybrid lexical + dense retrieval

---

## 8. Design Philosophy

The implementation prioritizes:

- local reproducibility
- measurable evaluation
- simple architecture
- citation accuracy
- conservative answer behavior

For this assessment, a clear and reliable baseline was favored over unnecessary complexity.
