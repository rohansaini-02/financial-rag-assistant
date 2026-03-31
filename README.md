# Investment Intelligence AI

A Retrieval-Augmented Generation (RAG) system for querying investment textbooks and financial PDFs. It extracts context using local vector embeddings and generates grounded, source-backed answers using Groq's Llama-3 model.

## Tech Stack
- **Frontend**: Streamlit
- **LLM**: Groq API (`llama-3.3-70b-versatile`)
- **Vector Storage**: FAISS (local)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)

## How to Run

1. **Clone the repo**
```bash
git clone https://github.com/rohansaini-02/financial-rag-assistant.git
cd financial-rag-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Add API Key**
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_key_here
```

4. **Start the app**
```bash
streamlit run streamlit_app.py
```

## Usage

1. **Launch the dashboard:** Open your browser and navigate to `http://localhost:8501`.
2. **Upload your document:** Drag and drop an investment textbook PDF into the provided upload zone.
3. **Wait for ingestion:** The system will quickly process the PDF and build the local context.
4. **Start analyzing:** Type your financial questions into the bottom chat bar, or click one of the suggested query chips to see instant, source-backed answers.
