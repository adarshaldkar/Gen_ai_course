# 🧩 Day 16: Text Chunking Strategies for RAG

This module demonstrates three essential text chunking strategies used in Retrieval-Augmented Generation (RAG) pipelines using `langchain-text-splitters`.

---

## 📑 Included Chunking Strategies

### 1. 📏 Fixed-Size Chunking
- **Class**: `CharacterTextSplitter(separator="", chunk_size=100, chunk_overlap=0)`
- **Behavior**: Splits text strictly by character length (`chunk_size=100`) regardless of word or sentence boundaries.
- **Use Case**: Fast baseline chunking when document structure is unstructured or uniform.

### 2. 📑 Paragraph Chunking
- **Class**: `CharacterTextSplitter(separator="\n\n", chunk_size=100, chunk_overlap=0)`
- **Behavior**: Splits text along paragraph breaks (`\n\n`), preserving paragraph-level semantic unity.
- **Use Case**: Articles, essays, and documents organized into distinct paragraphs.

### 3. 🔄 Recursive Character Chunking
- **Class**: `RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)`
- **Behavior**: Hierarchically splits text by paragraph (`\n\n`), sentence (`\n`), word (` `), and character while preserving context overlap across chunks (`chunk_overlap=20`).
- **Use Case**: Recommended default strategy for RAG vector search to prevent context loss at chunk boundaries.

---

## 🚀 How to Run

```bash
cd "week3/day16"
uv run python .\chunk.py
```
