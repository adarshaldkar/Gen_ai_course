import sys
import os
import json
import warnings
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

# Ensure UTF-8 stdout encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Suppress warnings
warnings.filterwarnings("ignore")

# 1. Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=groq_api_key)
eval_model = "openai/gpt-oss-120b"


# 2. Pydantic Models for Structured Evaluation Scores
class EvaluationResult(BaseModel):
    faithfulness_score: float = Field(description="Score from 0 to 100 on whether the answer is strictly based on context without hallucination")
    answer_relevance_score: float = Field(description="Score from 0 to 100 on how directly the answer addresses the user query")
    context_relevance_score: float = Field(description="Score from 0 to 100 on whether the retrieved context is relevant to the user query")
    reasoning: str = Field(description="Detailed explanation justifying the evaluation scores")


# 3. Core RAG Evaluation Function (LLM-as-a-Judge)
def evaluate_rag(question: str, context: str, answer: str) -> EvaluationResult:
    system_prompt = """
You are an expert AI RAG Evaluator specializing in LLM evaluation (RAG Triad).

Evaluate the RAG response across 3 core metrics (0 to 100):

1. **Faithfulness / Groundedness** (0-100): Is the answer fully supported ONLY by the provided context? (Lower score if there are hallucinations or unbacked claims).
2. **Answer Relevance** (0-100): Does the answer directly address the user's question?
3. **Context Relevance** (0-100): Does the retrieved context contain the information needed to answer the question?

Output strictly valid JSON matching this schema:
{
  "faithfulness_score": <number 0-100>,
  "answer_relevance_score": <number 0-100>,
  "context_relevance_score": <number 0-100>,
  "reasoning": "<detailed feedback>"
}
"""

    user_prompt = f"""
--- RAG EVALUATION CASE ---
USER QUESTION:
{question}

RETRIEVED CONTEXT:
{context}

GENERATED ANSWER:
{answer}
"""

    response = client.chat.completions.create(
        model=eval_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    result_json = json.loads(response.choices[0].message.content)
    return EvaluationResult(**result_json)


# 4. Test RAG Evaluation Suite
if __name__ == "__main__":
    print("==================================================")
    print("      🚀 DAY 16: RAG EVALUATION SUITE           ")
    print("==================================================\n")

    test_cases = [
        {
            "id": "Case 1: Excellent Grounded RAG",
            "question": "How many days can employees work from home?",
            "context": "Employees are permitted to work remotely up to 2 days per week after completing 3 months probation.",
            "answer": "Employees can work remotely up to 2 days per week after completing 3 months of probation."
        },
        {
            "id": "Case 2: Hallucination / Low Faithfulness",
            "question": "What is the annual gym reimbursement amount?",
            "context": "Employees can claim Rs 2000 per month for home internet reimbursement.",
            "answer": "Employees receive Rs 5000 per month for gym reimbursement and free annual health checkups."
        },
        {
            "id": "Case 3: Irrelevant Answer",
            "question": "What is the notice period for full-time employees?",
            "context": "Full-time employees have a 90 day notice period.",
            "answer": "Our company was founded in 2020 and is headquartered in Bangalore."
        }
    ]

    for case in test_cases:
        print("-" * 60)
        print(f"📌 {case['id']}")
        print(f"❓ Question: {case['question']}")
        print(f"📖 Context : {case['context']}")
        print(f"🤖 Answer  : {case['answer']}")
        print("\nEvaluating RAG Triad Metrics...")

        eval_res = evaluate_rag(case['question'], case['context'], case['answer'])

        print(f"\n📊 EVALUATION SCORES:")
        print(f"  • Faithfulness Score     : {eval_res.faithfulness_score}/100")
        print(f"  • Answer Relevance Score : {eval_res.answer_relevance_score}/100")
        print(f"  • Context Relevance Score: {eval_res.context_relevance_score}/100")
        print(f"  • Reasoning              : {eval_res.reasoning}\n")

    print("==================================================")
    print("      ✅ RAG EVALUATION COMPLETED                ")
    print("==================================================")
