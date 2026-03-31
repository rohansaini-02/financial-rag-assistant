"""
Configuration settings for the RAG pipeline.
All tunable parameters are centralized here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# ──────────────────────────────────────────────
# API Keys
# ──────────────────────────────────────────────
# Groq API Key (for lightning-fast LLM)
# Set your API key in the .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ──────────────────────────────────────────────
# Model Configurations
# ──────────────────────────────────────────────
# LLM Model (using Groq for speed)
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.1

# Embedding Model (LOCAL HuggingFace)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ──────────────────────────────────────────────
# RAG Configurations
# ──────────────────────────────────────────────
# Chunking settings
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 200
SEPARATORS = ["\n\n", "\n", ". ", " "]

# Retrieval settings
TOP_K = 5

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIRECTORY = BASE_DIR
FAISS_INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")