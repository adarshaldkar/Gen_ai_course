# Week 5 Day 20 — Single Agent vs Multi-Agent Token Efficiency Benchmark

## 📌 Overview
This project presents an empirical benchmark comparing a **Single Agent Architecture** against a **Multi-Agent Architecture** on token efficiency, execution speed, and response accuracy for a multi-step reasoning task involving information retrieval and mathematical calculation.

---

## 🏗️ Architecture Comparison

### 1. Single Agent Architecture (`single_agent.py`)
- **Design**: A single LLM operating with a ReAct (Reason + Act) loop equipped with both `web_search` and `calculate` tools.
- **Workflow**:
  1. Accepts user prompt into a unified context window.
  2. Decides dynamically whether to invoke search or calculation.
  3. Produces final answer directly.
- **Pros**: Low prompt overhead, simple control flow, lower overall token usage for simple tasks.
- **Cons**: Single context window grows rapidly on long multi-turn interactions.

```
User Query ---> [ Single Agent LLM + ReAct Tools ] ---> Final Output
```

---

### 2. Multi-Agent Architecture (`multiagent.py`)
- **Design**: Specialized agent decomposition orchestrated by a Manager Agent with shared file-based memory (`notes.md`).
- **Agents**:
  - **Search Specialist Agent**: Dedicated system prompt optimized for Tavily web search. Extracts raw numeric facts and writes findings to `notes.md`.
  - **Math Specialist Agent**: Dedicated system prompt optimized for math evaluation. Reads facts from `notes.md`, runs math tools, and appends calculations to `notes.md`.
  - **Manager Agent**: Reads the final state from `notes.md` and synthesizes the user-facing output.
- **Workflow**:
  ```
  User Query ---> [ Search Agent ] ---> (Write to notes.md)
                         |
                         v
                 [ Math Agent ]   ---> (Append to notes.md)
                         |
                         v
                 [ Manager Agent ] ---> Final Output
  ```
- **Pros**: Isolated agent focus, clean domain separation, maintainable and inspectable shared state (`notes.md`).
- **Cons**: Higher token consumption due to repeated system prompt overhead and memory context handoffs.

---

## 🛠️ Tools & Components (`tools.py`)

- **`TokenTracker`**: Accumulates exact `prompt_tokens`, `completion_tokens`, `total_tokens`, and `llm_calls` from Groq API completion responses.
- **`web_search(query)`**: Integrates Tavily API for precise search snippet retrieval.
- **`calculate(expression)`**: Evaluates arithmetic and math expressions safely.
- **`notes.md`**: Shared memory markdown buffer passed between specialized agents.

---

## 📊 Benchmark Results & Findings

### Test Query
> *"Find the height of Eiffel Tower and Burj Khalifa in meters, calculate their height difference in meters, and determine how many Eiffel Towers stacked on top of each other equal the height of Burj Khalifa."*

### Empirical Benchmark Output

| Metric | Single Agent | Multi-Agent System |
| :--- | :--- | :--- |
| **Total LLM Calls** | `1` | `3` |
| **Prompt Tokens** | `339` | `739` |
| **Completion Tokens** | `364` | `560` |
| **Total Tokens Consumed** | `703` | `1299` |
| **Execution Time** | `~1.94s` | `~2.46s` |

### Key Analytical Takeaways
1. **Token Overhead**: Multi-Agent system used **~84.8% more total tokens** (1299 vs 703 tokens) for a simple multi-step query.
2. **Context Amplification**: System prompts and context summaries are re-transmitted across each specialized agent call.
3. **When to use Multi-Agent**:
   - Complex workflows requiring distinct tool domains or security boundaries.
   - Long-horizon workflows where a single context window becomes saturated or noisy.
   - Team/Organization setups requiring parallel processing or independent agent auditing.

---

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   uv add groq tavily-python python-dotenv
   ```

2. **Configure Environment (`.env`)**:
   ```env
   GROQ_API_KEY=gsk_...
   TAVILY_API_KEY=tvly-...
   ```

3. **Run Benchmark Script**:
   ```bash
   uv run python main.py
   ```
