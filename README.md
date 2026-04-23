# Artikate Studio AI/ML Engineer Assessment

This repository contains my completed submission for the Artikate Studio AI / ML / LLM Engineer technical assessment. The work covers system diagnosis, retrieval-augmented generation, low-latency machine learning, and written systems design.

---

## Repository Structure

ARTIKATE_ASSESSMENT/

- section1/ → LLM pipeline diagnosis and reasoning  
- section2/ → Legal document RAG pipeline  
- section3/ → Ticket classifier under latency constraints  
- section4/ → Systems design written responses  

Root documentation:

- README.md → setup and execution guide  
- DESIGN.md → Section 2 architectural decisions  

---

## Environment

- Python 3.10+
- CPU execution supported
- Tested locally on Windows

Install dependencies separately inside each runnable section.

---

## Section 1 — Diagnose a Failing LLM Pipeline

Written answers are available in:

`section1/ANSWERS.md`

This section covers:

- hallucinated pricing responses
- multilingual language switching issues
- latency degradation over time
- stakeholder-facing postmortem summary

---

## Section 2 — Build a Production-Grade RAG Pipeline

A local Retrieval Augmented Generation pipeline for legal PDF search with source citations.

Implemented pipeline:

- PDF ingestion
- page-level chunking with overlap
- semantic embeddings
- FAISS vector retrieval
- confidence scoring
- grounded answers with citations
- precision@3 evaluation harness
- refusal handling when context is insufficient

Documentation:

- `DESIGN.md`

### Run Section 2

    cd section2
    pip install -r requirements.txt
    python evaluate.py ./data/sample_pdfs --index ./index

### Output

Returns:

- precision@3 score
- per-question retrieval results
- source references

Observed evaluation result:

- Precision@3: 1.00 (10/10 on evaluation set)

---

## Section 3 — Ticket Classifier Under Latency Constraints

Implemented a lightweight CPU-friendly classifier for automated support ticket routing.

### Objective

Classify incoming tickets into five categories while keeping inference under the required 500ms CPU latency budget.

Target labels:

- billing
- technical_issue
- feature_request
- complaint
- other

### Chosen Approach

Model used:

- TF-IDF vectorization
- Logistic Regression classifier

Why this approach:

- fast CPU inference
- strong baseline for short text classification
- simple deployment with minimal dependencies
- interpretable feature weights
- low memory footprint

Transformer fine-tuning was intentionally avoided because the added complexity and latency overhead were unnecessary for this problem size.

### Dataset

- synthetic labeled dataset generated using `generate_data.py`
- balanced samples across all five classes
- train / test split used for held-out evaluation

### Run Section 3

    cd section3
    pip install -r requirements.txt
    python generate_data.py
    python train.py
    python evaluate.py
    python test_latency.py

### Output

Reports:

- accuracy
- per-class precision / recall / F1
- confusion matrix
- latency validation

Observed evaluation result:

- Accuracy: 98.5%
- CPU inference comfortably below 500ms per ticket

### Known Confusions

Minor overlap may occur between:

- complaint vs billing
- complaint vs technical_issue

This is expected when users express frustration while also describing a service or product issue.

### Future Improvements

- larger real-world labeled dataset
- n-gram and text normalization improvements
- probability calibration
- transformer upgrade if latency budget increases

---

## Section 4 — Written Systems Design Review

Written answers are available in:

`section4/ANSWERS.md`

This section contains selected responses covering:

- prompt injection and LLM security
- LLM output quality evaluation framework

---

## Design Philosophy

Where trade-offs existed, I prioritized reproducibility, local execution, measurable evaluation, and practical production constraints over unnecessary complexity.

---

## Notes

- Generated artifacts such as `model.pkl`, `data.csv`, `index.faiss`, and `index.meta` are excluded from version control and can be recreated locally.
- No API keys are required for this submission.
- All runnable sections were tested locally from a clean environment.

---

## Submission Checklist

Included:

- all four required sections
- runnable code for Sections 2 and 3
- written answers for Sections 1 and 4
- design documentation for Section 2
- evaluation scripts and metrics
- local setup instructions