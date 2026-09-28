import os
import math
import re
from typing import Dict, Any
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

class TokenTracker:
    def __init__(self, name: str = "Agent"):
        self.name = name
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.llm_calls = 0

    def add_usage(self, usage: Any) -> None:
        """Accumulates token usage from Groq completion usage object."""
        if usage:
            p = getattr(usage, "prompt_tokens", 0) or 0
            c = getattr(usage, "completion_tokens", 0) or 0
            t = getattr(usage, "total_tokens", 0) or (p + c)
            self.prompt_tokens += p
            self.completion_tokens += c
            self.total_tokens += t
            self.llm_calls += 1

    def get_summary(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "llm_calls": self.llm_calls,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }

    def reset(self) -> None:
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.llm_calls = 0

    def print_summary(self) -> None:
        print(f"\n--- {self.name} Token Usage ---")
        print(f"Total LLM Calls    : {self.llm_calls}")
        print(f"Prompt Tokens      : {self.prompt_tokens}")
        print(f"Completion Tokens  : {self.completion_tokens}")
        print(f"Total Tokens       : {self.total_tokens}")


def web_search(query: str, max_results: int = 2) -> str:
    """Performs a web search using Tavily API and returns text summary."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY not configured."
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)
        results = response.get("results", [])
        if not results:
            return "No relevant search results found."
        
        snippets = []
        for r in results:
            title = r.get("title", "No Title")
            content = r.get("content", "")
            snippets.append(f"[{title}]: {content}")
        return "\n\n".join(snippets)
    except Exception as e:
        return f"Error executing web search: {str(e)}"


def calculate(expression: str) -> str:
    """Evaluates mathematical expressions safely using math operations."""
    try:
        # Clean expression
        clean_expr = expression.strip()
        # Restrict globals and builtins for safety
        allowed_globals = {"__builtins__": None}
        allowed_locals = {
            "abs": abs, "round": round, "min": min, "max": max,
            "pow": pow, "sqrt": math.sqrt, "ceil": math.ceil,
            "floor": math.floor, "pi": math.pi, "e": math.e
        }
        result = eval(clean_expr, allowed_globals, allowed_locals)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression '{expression}': {str(e)}"
