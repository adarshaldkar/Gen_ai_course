import os
import sys
import time
from dotenv import load_dotenv
from tools import TokenTracker
from single_agent import run_single_agent
from multiagent import run_multi_agent

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

TEST_QUERY = (
    "Find the height of Eiffel Tower and Burj Khalifa in meters, "
    "calculate their height difference in meters, "
    "and determine how many Eiffel Towers stacked on top of each other equal the height of Burj Khalifa."
)


def print_comparison_table(single_tracker: TokenTracker, multi_tracker: TokenTracker):
    """Prints a comparison table between Single Agent and Multi-Agent token usage."""
    s_s = single_tracker.get_summary()
    m_s = multi_tracker.get_summary()

    print("\n" + "=" * 70)
    print("=== BENCHMARK TOKEN EFFICIENCY COMPARISON SUMMARY ===")
    print("=" * 70)
    
    header = f"{'Metric':<25} | {'Single Agent':<18} | {'Multi-Agent System':<18}"
    divider = "-" * len(header)
    print(header)
    print(divider)
    
    print(f"{'Total LLM Calls':<25} | {s_s['llm_calls']:<18} | {m_s['llm_calls']:<18}")
    print(f"{'Prompt Tokens':<25} | {s_s['prompt_tokens']:<18} | {m_s['prompt_tokens']:<18}")
    print(f"{'Completion Tokens':<25} | {s_s['completion_tokens']:<18} | {m_s['completion_tokens']:<18}")
    print(f"{'Total Tokens Consumed':<25} | {s_s['total_tokens']:<18} | {m_s['total_tokens']:<18}")
    
    print(divider)
    
    if s_s['total_tokens'] > 0:
        diff = m_s['total_tokens'] - s_s['total_tokens']
        pct = (diff / s_s['total_tokens']) * 100
        direction = "more" if diff >= 0 else "fewer"
        print(f"Token Difference        : Multi-Agent used {abs(diff)} tokens ({abs(pct):.1f}%) {direction} than Single Agent.")
    print("=" * 70 + "\n")


def main():
    print("\n========================================================")
    print(">>> WEEK 5 DAY 20: SINGLE AGENT VS MULTI-AGENT BENCHMARK <<<")
    print("========================================================")
    print(f"Test Query: '{TEST_QUERY}'\n")

    # 1. Run Single Agent Benchmark
    single_tracker = TokenTracker("Single Agent")
    t0_single = time.time()
    single_res = run_single_agent(TEST_QUERY, single_tracker)
    t1_single = time.time()
    single_duration = t1_single - t0_single

    # 2. Run Multi-Agent Benchmark
    multi_tracker = TokenTracker("Multi-Agent System")
    t0_multi = time.time()
    multi_res = run_multi_agent(TEST_QUERY, multi_tracker)
    t1_multi = time.time()
    multi_duration = t1_multi - t0_multi

    # 3. Print Final Answers
    print("\n" + "="*50)
    print(">>> SINGLE AGENT FINAL ANSWER:")
    print("="*50)
    print(single_res)

    print("\n" + "="*50)
    print(">>> MULTI-AGENT FINAL ANSWER:")
    print("="*50)
    print(multi_res)

    # 4. Print Token Comparison Table
    print_comparison_table(single_tracker, multi_tracker)
    
    print(f"Single Agent Execution Time : {single_duration:.2f}s")
    print(f"Multi-Agent Execution Time  : {multi_duration:.2f}s")


if __name__ == "__main__":
    main()
