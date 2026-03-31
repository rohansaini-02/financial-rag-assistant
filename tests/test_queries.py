import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Test Queries Script
Runs all 5 mandatory test queries from the PRD and displays results.
"""

from backend.rag_pipeline import RAGPipeline


# ──────────────────────────────────────────────
# Mandatory Test Queries (from PRD Section 6)
# ──────────────────────────────────────────────
MANDATORY_QUERIES = [
    "how to deal with brokerage houses?",
    "what is theory of diversification?",
    "how to become intelligent investor?",
    "how to do business valuation?",
    "what is putting all eggs in one basket analogy?",
]


def run_test_queries():
    """Run all mandatory queries and display results."""
    
    print("\n" + "=" * 70)
    print("  RAG System (Groq) -- Mandatory Test Queries")
    print("=" * 70)
    
    # Initialize pipeline
    pipeline = RAGPipeline()
    pipeline.initialize()
    
    # Run each query
    for i, query in enumerate(MANDATORY_QUERIES, 1):
        print("\n" + "=" * 70)
        print(f"  TEST QUERY {i} of {len(MANDATORY_QUERIES)}")
        print(f"  Question: {query}")
        print("=" * 70)
        
        result = pipeline.query(query, verbose=True)
        
        print("\n" + "-" * 70)
        print("GENERATED ANSWER:")
        print("-" * 70)
        print(result["answer"])
        print("-" * 70)
    
    print("\n" + "=" * 70)
    print("  All test queries completed!")
    print("=" * 70)
    
    # Bonus: Test fallback behavior
    print("\n" + "=" * 70)
    print("  FALLBACK TEST -- Question NOT in document")
    print("=" * 70)
    
    fallback_query = "What is the weather forecast for tomorrow?"
    print(f"  Question: {fallback_query}")
    
    result = pipeline.query(fallback_query, verbose=False)
    
    print(f"\n   ANSWER: {result['answer']}")
    
    expected_fallback = "not found in document"
    if expected_fallback in result["answer"].lower():
        print("   Fallback test PASSED -- correctly responded with 'Not found in document'")
    else:
        print("   Fallback test WARNING -- response may not follow fallback pattern")
    
    print("=" * 70)


if __name__ == "__main__":
    run_test_queries()
