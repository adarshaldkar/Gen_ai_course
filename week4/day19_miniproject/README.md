# 🍕 Day 19 Mini-Project: Restaurant Order Management LangGraph Agent

An interactive, multi-node restaurant ordering and kitchen workflow agent built with **LangGraph** and **Groq** (`openai/gpt-oss-120b`).

---

## 🔄 State Machine & Execution Flow

```text
user_input ──► llm ──► order_confirm ──► llm ──► cook ──► llm ──► serve ──► llm ──► END
```

- **`llm` Node**: The central brain that inspects state, handles intent extraction, partial stock negotiations, and user dialogue.
- **`order_confirm` Node**: Validates dish inventory and stock availability.
- **`cook` Node**: Simulates kitchen preparation status.
- **`serve` Node**: Manages order dispatch and table serving.

---

## 🚀 How to Run

### Interactive Session
```bash
cd "week4/day19_miniproject"
uv run python .\restproject.py
```

### Scripted Scenario Simulation
```bash
uv run python -c "import restproject; restproject.simulate(['I want 2 pizzas', 'yes'])"
```
