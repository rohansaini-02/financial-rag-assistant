"""
PDF Document Ingestion Module
Loads and parses PDF documents from the configured directory.
"""

import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from config import PDF_DIRECTORY


def load_pdfs(target: str = None) -> list:
    """
    Load PDF file(s) from a directory or a specific path.
    
    Args:
        target: Path to a directory or a specific PDF file.
                Defaults to PDF_DIRECTORY from config.
    
    Returns:
        List of Document objects.
    """
    if target and os.path.isfile(target):
        pdf_files = [target]
    else:
        directory = target or PDF_DIRECTORY
        pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found at '{target or directory}'")
    
    all_documents = []
    for pdf_path in pdf_files:
        print(f"   Loading: {os.path.basename(pdf_path)}...")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        for doc in documents:
            doc.metadata["source_file"] = os.path.basename(pdf_path)
        all_documents.extend(documents)
    
    return all_documents



if __name__ == "__main__":
    # Quick test
    docs = load_pdfs()
    if docs:
        print(f"\nSample from page 1:\n{docs[0].page_content[:500]}...")
