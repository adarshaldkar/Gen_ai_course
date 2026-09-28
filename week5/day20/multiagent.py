import os
import sys
import re
from typing import Dict, Any
from dotenv import load_dotenv
from groq import Groq
from tools import TokenTracker, web_search, calculate

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

NOTES_FILE_PATH = os.path.join(os.path.dirname(__file__), "notes.md")

# System prompts for specialized agents
SEARCH_AGENT_PROMPT = """You are a Search Specialist Agent.
Your sole job is to search the web for accurate factual information and report raw facts.
You have access to:
ACTION: SEARCH: <query>

CRITICAL RULES:
- Do NOT output raw JSON function calls.
- Issue SEARCH actions strictly as plain text: ACTION: SEARCH: <query>
- Once you have gathered the required facts, respond with:
  FINAL FACTS: <list of key facts discovered>
"""

MATH_AGENT_PROMPT = """You are a Math & Quantitative Specialist Agent.
Your sole job is to perform accurate mathematical computations using tool calculations.
You have access to:
ACTION: CALCULATE: <python math expression>

CRITICAL RULES:
- Do NOT output raw JSON function calls.
- Issue CALCULATE actions strictly as plain text: ACTION: CALCULATE: <expression>
- Once done, respond with:
  FINAL MATH RESULTS: <summary of mathematical calculations>
"""

MANAGER_AGENT_PROMPT = """You are the Manager Agent orchestrating sub-specialist agents.
Your goal is to ensure the user query is completely answered by synthesizing work done by specialist agents and stored in shared memory.

Given the initial user request and shared memory notes, produce a comprehensive, well-structured FINAL ANSWER for the user.
Format your output as:
FINAL ANSWER: <detailed response addressing all parts of user query>
"""


def init_notes():
    """Initializes clean shared memory file."""
    with open(NOTES_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("# Multi-Agent Shared Memory Notes\n\n")


def read_notes() -> str:
    """Reads current contents of shared memory file."""
    if not os.path.exists(NOTES_FILE_PATH):
        return ""
    with open(NOTES_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def append_to_notes(section: str, content: str):
    """Appends a section to shared memory file."""
    with open(NOTES_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(f"## {section}\n{content.strip()}\n\n")


def run_search_agent(subtask: str, tracker: TokenTracker, client: Groq, model: str) -> str:
    """Runs the Search Specialist Agent."""
    print(f"\n[Search Specialist] Handling subtask: '{subtask}'")
    messages = [
        {"role": "system", "content": SEARCH_AGENT_PROMPT},
        {"role": "user", "content": f"Task: {subtask}"}
    ]
    
    for step in range(1, 4):
        response = client.chat.completions.create(model=model, messages=messages, temperature=0.1)
        tracker.add_usage(response.usage)
        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        
        if "FINAL FACTS:" in reply:
            facts = reply.split("FINAL FACTS:")[-1].strip()
            append_to_notes("Search Specialist Findings", facts)
            return facts

        action_match = re.search(r"ACTION:\s*SEARCH:\s*(.+)", reply, re.IGNORECASE)
        if action_match:
            query = action_match.group(1).strip()
            print(f"--> [Search Specialist] Executing Search: '{query}'")
            obs = web_search(query)
            messages.append({"role": "user", "content": f"OBSERVATION: {obs}"})
        else:
            messages.append({"role": "user", "content": "Provide ACTION: SEARCH: <query> or FINAL FACTS: <facts>"})
            
    facts = "Search Specialist completed max steps."
    append_to_notes("Search Specialist Findings", facts)
    return facts


def run_math_agent(subtask: str, context: str, tracker: TokenTracker, client: Groq, model: str) -> str:
    """Runs the Math Specialist Agent."""
    print(f"\n[Math Specialist] Handling subtask: '{subtask}'")
    messages = [
        {"role": "system", "content": MATH_AGENT_PROMPT},
        {"role": "user", "content": f"Context from notes:\n{context}\n\nTask: {subtask}"}
    ]
    
    for step in range(1, 4):
        response = client.chat.completions.create(model=model, messages=messages, temperature=0.1)
        tracker.add_usage(response.usage)
        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        
        if "FINAL MATH RESULTS:" in reply:
            results = reply.split("FINAL MATH RESULTS:")[-1].strip()
            append_to_notes("Math Specialist Calculations", results)
            return results

        action_match = re.search(r"ACTION:\s*CALCULATE:\s*(.+)", reply, re.IGNORECASE)
        if action_match:
            expr = action_match.group(1).strip()
            print(f"--> [Math Specialist] Executing Calculation: '{expr}'")
            obs = calculate(expr)
            messages.append({"role": "user", "content": f"OBSERVATION: {obs}"})
        else:
            messages.append({"role": "user", "content": "Provide ACTION: CALCULATE: <expr> or FINAL MATH RESULTS: <summary>"})
            
    results = "Math Specialist completed max steps."
    append_to_notes("Math Specialist Calculations", results)
    return results


def run_multi_agent(user_query: str, tracker: TokenTracker, model: str = "openai/gpt-oss-120b") -> str:
    """Executes Multi-Agent system with Manager, Search Specialist, Math Specialist & Shared Memory."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured in environment.")

    client = Groq(api_key=api_key)
    init_notes()

    print("\n" + "="*50)
    print(">>> STARTING MULTI-AGENT EXECUTION <<<")
    print("="*50)

    # Step 1: Search Agent gathers factual data
    search_subtask = "Find the exact height of the Eiffel Tower in meters and the height of Burj Khalifa in meters."
    search_facts = run_search_agent(search_subtask, tracker, client, model)

    # Step 2: Math Agent reads shared memory & performs calculations
    current_notes = read_notes()
    math_subtask = "Calculate the height difference in meters between Burj Khalifa and Eiffel Tower, and calculate how many Eiffel Towers stacked equals Burj Khalifa height."
    math_results = run_math_agent(math_subtask, current_notes, tracker, client, model)

    # Step 3: Manager synthesizes final output
    print("\n[Manager Agent] Synthesizing final answer from Shared Memory...")
    final_notes = read_notes()
    
    manager_messages = [
        {"role": "system", "content": MANAGER_AGENT_PROMPT},
        {"role": "user", "content": f"User Query: {user_query}\n\nShared Memory Notes:\n{final_notes}"}
    ]
    
    response = client.chat.completions.create(model=model, messages=manager_messages, temperature=0.1)
    tracker.add_usage(response.usage)
    reply = response.choices[0].message.content.strip()
    
    if "FINAL ANSWER:" in reply:
        final_answer = reply.split("FINAL ANSWER:")[-1].strip()
    else:
        final_answer = reply
        
    return final_answer


if __name__ == "__main__":
    tracker = TokenTracker("Multi-Agent Test")
    test_q = "Find the height of Eiffel Tower and Burj Khalifa in meters, calculate their height difference in meters, and determine how many Eiffel Towers stacked equal Burj Khalifa."
    res = run_multi_agent(test_q, tracker)
    print("\nFinal Result:\n", res)
    tracker.print_summary()
