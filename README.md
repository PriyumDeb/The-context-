# The-context- 
## A RAG BASED SYSTEM 🐋
*Builded on parent - child arcitcture *
*Builded by PRIYUM DEB*
## Overview
**The Context** is a production-ready, fully local Retrieval-Augmented Generation (RAG) pipeline designed to extract, process, and query highly complex PDF documents. 

Unlike naive RAG systems that blindly parse text and destroy document formatting, this system utilizes a layout-aware extraction method and a strict parent-child chunking strategy. It successfully differentiates between standard paragraphs and complex multi-row tables, ensuring that the local LLM receives perfectly structured, context-rich data for highly accurate answers.
as the current version it can handel more than 10 diffrent types pdf at once.
* #FEATURES
* **Layout-Preserving Extraction:** Differentiates between standard text blocks and tabular data, automatically converting tables into Markdown to maintain structural relationships.
*   **Contextual Chunking:** Uses a parent-child mapping structure to assign unique, traceable IDs and source metadata to every piece of extracted data.
*   **Multi-Document Processing:** Capable of ingesting and querying across 10+ multi-page PDFs simultaneously within a single local vector space.
*   **Fully Local Execution:** Operates entirely offline using local vector databases (ChromaDB) and local LLM inference, ensuring strict data privacy.

## Current Limitations
*   **Semantic Drift at Scale:** While the system comfortably handles a small batch of PDFs (10+), querying for exact page numbers or highly specific cross-document facts can occasionally return vague results. The engine currently relies purely on semantic keyword matching rather than explicit metadata filtering (e.g., SQL-style `where` clauses).
*   **Complex Table Edge Cases:** Standard tabular data is preserved, but highly irregular, merged, or nested PDF tables may still parse incorrectly.
*   **Interface:** The pipeline operates entirely via the terminal. There is currently no web interface or GUI for non-technical end users.
## System Architecture & File Structure

The pipeline is modular, split into three distinct scripts that handle data step-by-step:

*   **`pdf_semantic.py` (Ingestion & Extraction):** 
    The starting point of the pipeline. It reads the raw PDF files, preserves the physical page layout, and extracts text and tables. It cleans the raw data and structures it into Python dictionaries, assigning unique IDs and source metadata (like file name and page number) to every chunk.

*   **`vectordb.py` (Storage & Indexing):** 
    The database router. It takes the structured dictionaries from the ingestion script, generates dense vector embeddings for the text, and commits everything into a local ChromaDB collection. It ensures that the metadata remains attached to the vector data for accurate retrieval.

*   **`search.py` (Retrieval & Generation):** 
    The inference engine. It takes a user's question, searches the ChromaDB collection for the most mathematically relevant text chunks, and stitches that text together with its metadata. It then injects this formatted context into a strict prompt for the local LLM (Gemma) to generate a grounded answer.
