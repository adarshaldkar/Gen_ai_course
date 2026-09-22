# 🕸️ Day 18: Introduction to LangGraph StateGraph Architecture

This module introduces **LangGraph**, a framework for building stateful, multi-actor applications with LLMs using graph-based control flows.

---

## 💡 Concepts Demonstrated

- **`TypedDict` State**: Defining shared state (`State` with `number: int`) passed between graph nodes.
- **Nodes (`StateGraph.add_node`)**: Discrete function steps (`double` and `finish`).
- **Conditional Edges (`StateGraph.add_conditional_edges`)**: Routing logic (`decision`) that dynamically determines the next node based on state values:
  - If `number < 100` $\rightarrow$ Loop back to `double`.
  - If `number >= 100` $\rightarrow$ Transition to `finish` and `END`.

---

## 🔄 Graph Flow Visualization

```text
[Start: 5] ──► double ──► (number < 100?) ──Yes──► double (5 -> 10 -> 20 -> 40 -> 80 -> 160)
                             │
                            No
                             ▼
                          finish ──► END (Final State: 160)
```

---

## 🚀 How to Run

```bash
cd "week4/day18"
uv run python .\langgraphintro.py
```
