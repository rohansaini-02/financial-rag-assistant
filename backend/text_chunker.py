"""
Text Chunking Module
Splits extracted document text into smaller semantic chunks
for embedding and retrieval.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS


def chunk_documents(documents: list) -> list:
    """
    Split documents into smaller chunks with overlap.
    
    Args:
        documents: List of Document objects from PDF loader.
    
    Returns:
        List of chunked Document objects with preserved metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add chunk index to metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
    
    print(f"\nChunking Results:")
    print(f"   Input documents: {len(documents)}")
    print(f"   Output chunks:   {len(chunks)}")
    print(f"   Chunk size:      {CHUNK_SIZE} chars")
    print(f"   Overlap:         {CHUNK_OVERLAP} chars")
    
    # Print sample chunk stats
    if chunks:
        lengths = [len(c.page_content) for c in chunks]
        print(f"   Avg chunk length: {sum(lengths) // len(lengths)} chars")
        print(f"   Min chunk length: {min(lengths)} chars")
        print(f"   Max chunk length: {max(lengths)} chars")
    
    return chunks


if __name__ == "__main__":
    from backend.pdf_loader import load_pdfs
    
    docs = load_pdfs()
    chunks = chunk_documents(docs)
    
    if chunks:
        print(f"\n--- Sample Chunk (index 0) ---")
        print(f"Content: {chunks[0].page_content[:300]}...")
        print(f"Metadata: {chunks[0].metadata}")
