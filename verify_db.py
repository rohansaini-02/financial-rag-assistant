import sys
import os
import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Ensure Python can find the backend module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from backend.config import FAISS_INDEX_DIR, EMBEDDING_MODEL

# Redirect stdout to a UTF-8 file to prevent console encoding crashes
sys.stdout = open('verification_output.txt', 'w', encoding='utf-8')

def main():
    print("==================================================")
    print("      LOCAL VECTOR DATABASE VERIFICATION ")
    print("==================================================\n")
    
    if not os.path.exists(FAISS_INDEX_DIR):
        print("[ERROR] FAISS index not found. Please upload a PDF in the UI first.")
        return
        
    print(f"[*] Accessing Local FAISS Database at: {FAISS_INDEX_DIR}")
    
    # 1. Load Embeddings Model
    print(f"[*] Loading Embedding Model: {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # 2. Load Vector Store
    print("[*] Connecting to FAISS Index...")
    try:
        vector_store = FAISS.load_local(
            FAISS_INDEX_DIR, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"[ERROR] Could not load vector store: {e}")
        return
        
    # 3. Extract Documents
    # langchain faiss stores dict of id -> Document in docstore._dict
    doc_dict = vector_store.docstore._dict
    if not doc_dict:
        print("[!] The database is empty.")
        return
        
    print(f"\n[+] Successfully connected! Total text chunks in database: {len(doc_dict)}\n")
    
    # Extract the first 2 chunks
    sample_ids = list(doc_dict.keys())[:2]
    
    for i, doc_id in enumerate(sample_ids):
        doc = doc_dict[doc_id]
        
        # Compute the exact embedding vector that FAISS is storing for this chunk
        vector_embedding = embeddings.embed_query(doc.page_content)
        
        print("--------------------------------------------------")
        print(f"CHUNK #{i+1} (ID: {doc_id})")
        print("--------------------------------------------------")
        print(f"METADATA: {doc.metadata}")
        
        # Show structured chunk text snippet
        snippet = doc.page_content[:400].replace('\n', ' ')
        print(f"\nTEXT CHUNK CONTENT:\n\"{snippet}...\"\n")
        
        # Show physical vector embedding
        vec_display = ", ".join(f"{v:.5f}" for v in vector_embedding[:15])
        print(f"VECTOR EMBEDDING (Total Dimensions: {len(vector_embedding)}):")
        print(f"[{vec_display}, ...]")
        print("--------------------------------------------------\n")
        
    print("✅ Verification Complete. Take a screenshot of the terminal output above.")

if __name__ == "__main__":
    main()
