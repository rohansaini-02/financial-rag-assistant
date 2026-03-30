"""
Semantic Retrieval Module
Performs similarity search on the FAISS vector store to find
the most relevant chunks for a given query.
"""

from langchain_community.vectorstores import FAISS
from config import TOP_K


def retrieve_relevant_chunks(vector_store: FAISS, query: str, top_k: int = None) -> list:
    """
    Retrieve the most relevant document chunks for a query.
    
    Args:
        vector_store: FAISS vector store to search.
        query: User's question string.
        top_k: Number of top results to retrieve. Defaults to TOP_K from config.
    
    Returns:
        List of tuples (Document, similarity_score), sorted by relevance.
    """
    k = top_k or TOP_K
    
    # Perform similarity search with scores
    results = vector_store.similarity_search_with_score(query, k=k)
    
    return results


def format_retrieved_context(results: list) -> str:
    """
    Format retrieved chunks into a single context string for the LLM.
    
    Args:
        results: List of (Document, score) tuples from similarity search.
    
    Returns:
        Formatted context string combining all retrieved chunks.
    """
    context_parts = []
    
    for i, (doc, score) in enumerate(results, 1):
        source = doc.metadata.get("source_file", "Unknown")
        page = doc.metadata.get("page", "N/A")
        context_parts.append(
            f"[Chunk {i}] (Source: {source}, Page: {page + 1 if isinstance(page, int) else page}, "
            f"Relevance Score: {score:.4f})\n{doc.page_content}"
        )
    
    return "\n\n---\n\n".join(context_parts)


def print_retrieved_chunks(results: list) -> None:
    """
    Pretty-print the retrieved chunks for debugging/inspection.
    
    Args:
        results: List of (Document, score) tuples from similarity search.
    """
    print(f"\n   Retrieved {len(results)} relevant chunks:\n")
    
    for i, (doc, score) in enumerate(results, 1):
        source = doc.metadata.get("source_file", "Unknown")
        page = doc.metadata.get("page", "N/A")
        page_display = page + 1 if isinstance(page, int) else page
        content_preview = doc.page_content[:200].replace("\n", " ")
        
        print(f"  Chunk {i}:")
        print(f"     Source: {source} | Page: {page_display}")
        print(f"     Score:  {score:.4f}")
        print(f"     Preview: {content_preview}...")
        print()
