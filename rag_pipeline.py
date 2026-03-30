"""
RAG Pipeline Orchestrator
Ties together all modules into a complete RAG pipeline.
"""

from pdf_loader import load_pdfs
from text_chunker import chunk_documents
from embedding_store import create_or_load_store
from retriever import retrieve_relevant_chunks, format_retrieved_context, print_retrieved_chunks
from llm_handler import generate_response


class RAGPipeline:
    """
    Complete Retrieval-Augmented Generation pipeline.
    
    Usage:
        pipeline = RAGPipeline()
        pipeline.initialize()
        answer, chunks = pipeline.query("What is diversification?")
    """
    
    def __init__(self):
        self.vector_store = None
        self.is_initialized = False
    
    def initialize(self, force_rebuild: bool = False, file_path: str = None):
        """
        Initialize the pipeline: load PDF, chunk, embed, and store.
        
        Args:
            force_rebuild: If True, rebuilds the index.
            file_path: Optional path to a specific PDF to process.
        """
        if force_rebuild or file_path:
            docs = load_pdfs(file_path) if file_path else load_pdfs()
            chunks = chunk_documents(docs)
            self.vector_store = create_or_load_store(chunks)
        else:
            try:
                self.vector_store = create_or_load_store()
            except (FileNotFoundError, ValueError):
                docs = load_pdfs()
                chunks = chunk_documents(docs)
                self.vector_store = create_or_load_store(chunks)
        
        self.is_initialized = True

    
    def query(self, question: str, verbose: bool = True) -> dict:
        """
        Process a user query through the full RAG pipeline.
        
        Args:
            question: User's question string.
            verbose: If True, prints retrieved chunks and details.
        
        Returns:
            Dictionary with 'answer', 'retrieved_chunks', and 'context'.
        """
        if not self.is_initialized:
            raise RuntimeError("Pipeline not initialized. Call initialize() first.")
        
        # Step 1: Retrieve relevant chunks
        results = retrieve_relevant_chunks(self.vector_store, question)
        
        if verbose:
            print_retrieved_chunks(results)
        
        # Step 2: Format context
        context = format_retrieved_context(results)
        
        # Step 3: Generate response using LLM
        if verbose:
            print("   Generating response...\n")
        
        answer = generate_response(context, question)
        
        return {
            "answer": answer,
            "retrieved_chunks": results,
            "context": context,
        }
