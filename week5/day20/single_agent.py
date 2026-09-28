import os
import sys
import re
from typing import Tuple
from dotenv import load_dotenv
from groq import Groq
from tools import TokenTracker, web_search, calculate

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

SINGLE_AGENT_SYSTEM_PROMPT = """You are an intelligent, autonomous problem-solving agent.
You have access to two tools to solve complex information gathering and math tasks:

1. SEARCH: <query>
Use this tool to find information on the web.
Example: SEARCH: Eiffel Tower height in meters

2. CALCULATE: <python math expression>
Use this tool to evaluate exact math expressions.
Example: CALCULATE: 828 - 330
Example: CALCULATE: 828 / 330

CRITICAL RULES:
- Do NOT output raw JSON tool calls. Format your responses STRICTLY as plain text.
- Respond in ONE of these formats per step:
  - Tool call format:
    THOUGHT: <your reasoning step>
    ACTION: SEARCH: <query>
    OR
    THOUGHT: <your reasoning step>
    ACTION: CALCULATE: <expression>
  - Final answer format:
    THOUGHT: <your final reasoning>
    FINAL ANSWER: <your detailed final response with steps and numbers>

- Perform only ONE tool action at a time.
- Be accurate and clear.
"""

def run_single_agent(user_query: str, tracker: TokenTracker, model: str = "openai/gpt-oss-120b", max_steps: int = 6) -> str:
    """Runs a single agent equipped with Search and Calculate tools."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured in environment.")

    client = Groq(api_key=api_key)
    
    messages = [
        {"role": "system", "content": SINGLE_AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    print("\n" + "="*50)
    print(">>> STARTING SINGLE AGENT EXECUTION <<<")
    print("="*50)

    for step in range(1, max_steps + 1):
        print(f"\n[Single Agent - Step {step}] Calling LLM...")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1
        )
        
        # Track token usage
        tracker.add_usage(response.usage)
        
        reply = response.choices[0].message.content.strip()
        print(f"Agent Response:\n{reply}\n")
        
        # Append assistant response to message history
        messages.append({"role": "assistant", "content": reply})

        # Check for Final Answer
        if "FINAL ANSWER:" in reply:
            final_ans = reply.split("FINAL ANSWER:")[-1].strip()
            return final_ans

        # Check for Tool Action
        action_match = re.search(r"ACTION:\s*(SEARCH|CALCULATE):\s*(.+)", reply, re.IGNORECASE)
        if action_match:
            tool_type = action_match.group(1).upper()
            tool_input = action_match.group(2).strip()
            
            print(f"--> Executing Tool: {tool_type} with input: '{tool_input}'")
            if tool_type == "SEARCH":
                tool_output = web_search(tool_input)
            elif tool_type == "CALCULATE":
                tool_output = calculate(tool_input)
            else:
                tool_output = f"Unknown tool: {tool_type}"
                
            print(f"--> Tool Output Snippet: {tool_output[:150]}...")
            
            # Feed tool observation back to assistant
            messages.append({"role": "user", "content": f"OBSERVATION: {tool_output}"})
        else:
            # If agent didn't output action or final answer properly, prompt it to proceed
            messages.append({
                "role": "user", 
                "content": "Please select a valid ACTION (SEARCH: <query> or CALCULATE: <expr>) or provide your FINAL ANSWER:"
            })

    return "Single Agent reached max steps without completing."


if __name__ == "__main__":
    tracker = TokenTracker("Single Agent Test")
    test_q = "Find the height of Eiffel Tower and Burj Khalifa, calculate their height difference, and ratio."
    res = run_single_agent(test_q, tracker)
    print("Result:", res)
    tracker.print_summary()
