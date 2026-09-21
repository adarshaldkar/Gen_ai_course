# 🚀 Generative AI & LLM Engineering Course

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![Package Manager](https://img.shields.io/badge/Package%20Manager-uv-purple.svg)](https://github.com/astral-sh/uv)
[![LLM Provider](https://img.shields.io/badge/LLM-Groq%20SDK-orange.svg)](https://console.groq.com)
[![Vector DB](https://img.shields.io/badge/Vector%20DB-Qdrant-red.svg)](https://qdrant.tech)
[![Framework](https://img.shields.io/badge/Framework-LangChain%20%7C%20FastAPI-green.svg)](https://fastapi.tiangolo.com)

Welcome to the **Generative AI & LLM Engineering Course** repository! This repository contains hands-on projects, daily code walkthroughs, agentic architectures, vector database implementations, and RAG pipelines built from first principles.

---

## 📅 Course Curriculum Roadmap

```text
gen_ai_course/
├── week 1/                  # Week 1: LLM Fundamentals & Structured Data
│   ├── day1/                # Groq API Setup & Hello LLM
│   ├── day2/                # System Messages, Roles & Temperature Tuning
│   ├── day3/                # Token Usage & Context Limits
│   ├── day4/                # Structured Extraction with Pydantic & JSON Mode
│   └── day5/                # 🏆 Mini-Project: Resume & Job Description Matcher
├── week 2/                  # Week 2: Prompting, Agents & Microservices
│   ├── day6/                # Prompt Engineering Frameworks
│   ├── day7/                # ReAct (Reasoning + Acting) Autonomous Agent Loop
│   ├── day8/                # Multi-Step Prompt Chaining Pipelines
│   └── day9/                # 🏆 Mini-Project: AI Candidate Interviewer API (FastAPI)
└── week3/                   # Week 3: Embeddings, Vector DBs & RAG Architecture
    ├── day10/               # Retrieval-Augmented Generation (RAG) Basics
    ├── day11/               # Dense Embeddings & Cosine Similarity (SentenceTransformer)
    ├── day12/               # Embedded RAG Pipeline
    ├── day14/               # Qdrant Vector Database Integration
    ├── day15/               # Metadata Payload Filtering in Qdrant
    └── day16/               # Text Chunking Strategies (Fixed, Paragraph, Recursive)
```

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Package Manager** | `uv` | Blazing fast Python package and environment manager |
| **Inference Engine** | `Groq SDK` | High-throughput LLM inference using LLaMA models |
| **Vector DB** | `Qdrant` | High-performance vector database with payload filtering |
| **Embeddings** | `SentenceTransformer` | Local dense vector embeddings (`all-MiniLM-L6-v2`) |
| **Text Splitters** | `langchain-text-splitters` | Chunking strategies for RAG optimization |
| **Web Framework** | `FastAPI` & `Uvicorn` | RESTful API endpoints for LLM microservices |
| **Data Validation** | `Pydantic` v2 | Schema validation & structured JSON outputs |

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/adarshaldkar/Gen_ai_course.git
cd Gen_ai_course
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
QDRANT_URL=https://your-qdrant-cluster-url.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
```

### 3. Run Any Day's Module
Navigate to the specific day and run with `uv`:
```bash
cd "week3/day16"
uv run python .\chunk.py
```

---

## 🌟 Key Project Highlights

- **🤖 Custom ReAct Agent (`week 2/day7`)**: Implements an autonomous agent reasoning loop (`Thought` $\rightarrow$ `Action` $\rightarrow$ `Observation` $\rightarrow$ `Final Answer`) from scratch using custom tool bindings.
- **📄 Resume Parser & Matcher (`week 1/day5`)**: Extracts structured JSON from PDF/DOCX resumes using Pydantic schemas and scores candidate compatibility against job descriptions.
- **⚡ Qdrant Vector DB RAG (`week 3/day14` & `day15`)**: Builds end-to-end vector retrieval pipelines featuring metadata filtering (`PayloadSchemaType.KEYWORD`).
- **🧩 Text Chunking Strategies (`week 3/day16`)**: Evaluates Fixed-Size, Paragraph, and Recursive Character chunking methods for RAG accuracy.

---

## 📝 License
This repository is created for educational purposes as part of the **Generative AI Engineering Course**.
