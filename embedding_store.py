"""
Embedding Generation & FAISS Vector Store Module
Creates embeddings from text chunks and stores them in a FAISS index.
Uses LOCAL HuggingFace embeddings (all-MiniLM-L6-v2) for FAST, offline embedding.
No API calls needed - runs entirely on your machine!
"""

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import FAISS_INDEX_DIR

# ──────────────────────────────────────────────
# Local Embedding Model (no API key needed!)
# ──────────────────────────────────────────────
LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Initialize the local HuggingFace embedding model.
    Runs entirely on your machine - no API calls, no rate limits!
    
    Returns:
        HuggingFaceEmbeddings instance using all-MiniLM-L6-v2.
    """
    return HuggingFaceEmbeddings(
        model_name=LOCAL_EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def create_vector_store(chunks: list) -> FAISS:
    """
    Create a FAISS vector store from document chunks.
    Uses local embeddings - completes in seconds, not minutes!
    
    Args:
        chunks: List of Document objects to embed and store.
    
    Returns:
        FAISS vector store instance.
    """
    print(f"\n   Generating embeddings for {len(chunks)} chunks...")
    print(f"   Using LOCAL model: {LOCAL_EMBEDDING_MODEL} (no API calls)")
    print(f"   This should complete in under a minute...")
    
    embeddings = get_embedding_model()
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )
    
    print(f"   Done! Vector store created with {len(chunks)} vectors")
    return vector_store


def save_vector_store(vector_store: FAISS, index_dir: str = None) -> None:
    """Save the FAISS vector store to disk for persistence."""
    directory = index_dir or FAISS_INDEX_DIR
    os.makedirs(directory, exist_ok=True)
    vector_store.save_local(directory)
    print(f"   Vector store saved to: {directory}")


def load_vector_store(index_dir: str = None) -> FAISS:
    """Load a previously saved FAISS vector store from disk."""
    directory = index_dir or FAISS_INDEX_DIR
    
    if not os.path.exists(directory):
        raise FileNotFoundError(
            f"No FAISS index found at '{directory}'. "
            "Please run the indexing pipeline first."
        )
    
    embeddings = get_embedding_model()
    vector_store = FAISS.load_local(
        directory,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    
    print(f"   Vector store loaded from: {directory}")
    return vector_store


def create_or_load_store(chunks: list = None) -> FAISS:
    """
    Smart loader: loads existing index if available, otherwise creates new one.
    
    Args:
        chunks: Document chunks (required only if creating a new store).
    
    Returns:
        FAISS vector store instance.
    """
    index_path = os.path.join(FAISS_INDEX_DIR, "index.faiss")
    
    if os.path.exists(index_path):
        print("   Existing FAISS index found. Loading...")
        return load_vector_store()
    else:
        if chunks is None:
            raise ValueError(
                "No existing index found and no chunks provided. "
                "Please provide document chunks to create a new index."
            )
        print("   No existing index found. Creating new vector store...")
        store = create_vector_store(chunks)
        save_vector_store(store)
        return store
