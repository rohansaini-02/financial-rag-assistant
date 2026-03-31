"""
LLM Integration & Response Generation Module
Handles prompt construction and LLM calls for answer generation.
Now uses GROQ SDK for lightning-fast responses.
"""

import time
from groq import Groq
from backend.config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE

# ──────────────────────────────────────────────
# Prompt Template (Optimized for RAG)
# ──────────────────────────────────────────────
RAG_PROMPT_TEMPLATE = """Context from document:
{context}

Question:
{question}

Instruction:
Answer ONLY using the provided context above. 
Keep your answer clear, educational, and professionally structured.
If the answer is NOT in the context, strictly say "Not found in document".
Do NOT mention "the context" or "the document" in your final answer - speak directly as an expert.
"""

def generate_response(context: str, question: str) -> str:
    """
    Generate an answer using the Groq LLM with retrieved context.
    Includes retry logic for robustness.
    """
    client = Groq(api_key=GROQ_API_KEY)
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a professional Financial Analyst and Investment Advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=LLM_TEMPERATURE,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait = 5 * (attempt + 1)
                print(f"   Groq Rate limit hit, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"   Groq Error: {str(e)}")
                return f"Error connecting to AI advisor: {str(e)}"
    
    return "Error: LLM failed to respond."
