# Investment Intelligence AI

An institutional-grade Retrieval-Augmented Generation (RAG) dashboard designed specifically for analyzing extensive financial and investment textbooks. 

This project allows analysts and students to upload complex financial PDFs, process them securely via local vector embeddings, and interactively query the text using the lightning-fast Groq (Llama-3 70B) inference engine.

## 🚀 Key Features
- **Instant Local Vectorization:** Uses HuggingFace's `all-MiniLM-L6-v2` and FAISS for 100% secure, local, and lightning-fast document vectorization. No source text is leaked to third-party embedding APIs.
- **Institutional-Grade UI:** A sleek, fully customized dark-mode Streamlit dashboard mirroring professional analytical data terminals.
- **Ultra-Fast Generation:** Powered by the **Groq API** running `llama-3.3-70b-versatile`, capable of generating comprehensive financial analysis in under 2 seconds.
- **Strict Source Grounding:** Completely eliminates hallucinations by forcefully citing exact passages and page numbers from the uploaded textbook. Defaults to "Not found in document" for out-of-scope inquiries.
- **Contextual Memory:** Full interactive conversational memory handled via Streamlit session states.

## 🛠️ Technology Stack
- **Frontend:** [Streamlit](https://streamlit.io/) (with custom injected React/CSS containers)
- **Vector Database:** [FAISS-CPU](https://github.com/facebookresearch/faiss)
- **Embeddings:** [HuggingFace via LangChain](https://python.langchain.com/) (`all-MiniLM-L6-v2`)
- **LLM / Inference:** [Groq Cloud](https://groq.com/) (`llama-3.3-70b-versatile`)
- **Document Processing:** `PyPDFLoader`, `RecursiveCharacterTextSplitter`

## ⚙️ Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/rohansaini-02/financial-rag-assistant.git
cd financial-rag-assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**4. Launch the Terminal**
```bash
streamlit run streamlit_app.py
```

## 📖 Usage Workflow
1. Run the application and open the local web server port (default: `http://localhost:8501`).
2. Drag and drop your investment textbook (PDF) into the target zone.
3. Wait momentarily for the RAG engine to parse, chunk, and embed the text locally.
4. Once the green "System Online" indicator appears, use the chat console or the preset suggestion chips (e.g., *"how to do business valuation?"*) to query the financial knowledge base.
