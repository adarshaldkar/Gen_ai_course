# 🤖 Day 17: Autonomous Function-Calling AI Agent

This module implements an autonomous function-calling AI agent using the Groq API and external tool definitions.

---

## 🛠️ Integrated Tools

1. **`web_search(query: str)`**: Uses `TavilyClient` to search the web for live, up-to-date real-world information.
2. **`calculate(expression: str)`**: Evaluates mathematical expressions using a secure Python `ast` (Abstract Syntax Tree) parser.

---

## 🔄 How the Agent Loop Works

```text
User Question ──► Groq LLM (tool_choice="auto") ──► Tool Call Request (JSON)
                                                          │
Final Answer ◄── Groq Second Pass ◄── Tool Result Output ◄┘
```

1. **Step 1**: The user query is sent to Groq with tool function definitions.
2. **Step 2**: If the model decides to call one or more tools, it returns `tool_calls` containing arguments.
3. **Step 3**: The local Python code executes the corresponding tool function (`web_search` or `calculate`).
4. **Step 4**: Tool execution outputs are appended to conversation history as `role="tool"`.
5. **Step 5**: Groq synthesizes the tool outputs into a final, user-friendly response.

---

## 🚀 How to Run

```bash
cd "week4/day17"
uv run python .\ai_agent.py
```
