import streamlit as st
import os
import tempfile
from rag_pipeline import RAGPipeline

st.set_page_config(
    page_title="Investment Intelligence AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# Stitch-Inspired CSS: "The Precision Monolith"
# ──────────────────────────────────────────────
st.markdown("""
    <style>
    :root {
        --background: #0E1117;
        --sidebar-bg: #101319;
        --text-primary: #FFFFFF;
        --text-secondary: #8b90a0;
        --accent-blue: #007BFF;
        --card-bg: #1D2026;
        --border-color: #32353C;
    }
    
    .stApp {
        background-color: var(--background);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Cruft */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stAppDeployButton {display:none;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-color);
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 1.5rem !important;
    }
    
    /* Main Area Adjustments */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
    }
    
    /* Typography */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        background-color: #191c22;
        color: #adc7ff;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        border: 1px solid var(--border-color);
    }
    
    /* Upload Card */
    .upload-card {
        background-color: var(--card-bg);
        border: 1px dashed #414754;
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Chips */
    .suggestion-chip {
        background-color: #191c22;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 10px 15px;
        color: var(--text-secondary);
        font-size: 0.85rem;
        text-align: center;
        margin-bottom: 10px;
        cursor: pointer;
    }
    
    /* Chat bubbles */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
    
    .source-box {
        background-color: var(--card-bg);
        border-left: 3px solid var(--accent-blue);
        padding: 15px;
        font-size: 0.85rem;
        color: #c1c6d7;
        margin-top: 10px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Session Initialization
# ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()
if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

# ──────────────────────────────────────────────
# Sidebar - Navigation & History
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h3 style='color: #007BFF; font-weight: 700; font-size: 1.2rem; margin-bottom: 0px;'>INVESTMENT INTELLIGENCE AI</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #414754; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 30px;'>INSTITUTIONAL GRADE RAG</p>", unsafe_allow_html=True)
    
    if st.button("➕ New Analysis", use_container_width=True):
        st.session_state.processed_file = None
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='color: #414754; font-size: 0.75rem; font-weight: 600;'>CHAT HISTORY</p>", unsafe_allow_html=True)
    
    history_container = st.container()

# ──────────────────────────────────────────────
# Top Header Bar
# ──────────────────────────────────────────────
col_tl, col_tr = st.columns([1, 1])
with col_tl:
    st.markdown("<span style='font-weight: 600; font-size: 1.1rem;'>Intelligence Terminal</span> &nbsp;|&nbsp; <span style='color: #10A37F; font-size: 0.7rem; font-weight: 800;'>● SYSTEM STATUS: READY</span>", unsafe_allow_html=True)
st.markdown("---")

# ──────────────────────────────────────────────
# Main UI - Rendering Immediately
# ──────────────────────────────────────────────
if not st.session_state.processed_file:
    # Split Layout (Hero & Upload)
    col_hero, col_upload = st.columns([1.2, 1])
    
    with col_hero:
        st.markdown("<div class='hero-title'>Precision<br>Investment<br>Intelligence.</div>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>AI-Powered Insights for Smarter Stock Market Decisions</div>", unsafe_allow_html=True)
        st.markdown("<span class='badge'>🔒 AES-256 Encrypted</span> <span class='badge'>🧠 Llama 3 Professional</span>", unsafe_allow_html=True)
        
    with col_upload:
        st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
        st.markdown("### 📄 Ingest Research Papers")
        st.markdown("<p style='color: #8b90a0; font-size: 0.9rem;'>Drag and drop PDF investment books to initialize the RAG engine.</p>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
        st.markdown("<p style='color: #414754; font-size: 0.7rem; margin-top: 15px; font-weight: 600;'>SUPPORTED FORMATS: PDF</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file:
            with st.status("Initializing RAG Engine...", expanded=True) as status:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    st.write("Extracting texts and generating FAISS embeddings...")
                    st.session_state.pipeline.initialize(file_path=tmp_path)
                    st.session_state.processed_file = uploaded_file.name
                    status.update(label="System Online.", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
    
    # Suggestion Chips
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='suggestion-chip'>how to deal with brokerage houses?</div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='suggestion-chip'>what is theory of diversification?</div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='suggestion-chip'>how to become intelligent investor?</div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='suggestion-chip'>how to do business valuation?</div>", unsafe_allow_html=True)

else:
    # ──────────────────────────────────────────────
    # Active Chat Mode
    # ──────────────────────────────────────────────
    st.success(f"**Active Document:** {st.session_state.processed_file}")
    
    # Display Chat History 
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("View Institutional Sources"):
                    for src in message["sources"]:
                        st.markdown(f"<div class='source-box'><b>Page {src['page']}</b><br>{src['content']}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Chat Input Bar
# ──────────────────────────────────────────────
if prompt := st.chat_input("Ask the AI about market theory or valuation..."):
    if not st.session_state.processed_file:
        st.error("Please explicitly upload a document in the box above to start querying.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Extracting insights..."):
                try:
                    result = st.session_state.pipeline.query(prompt, verbose=False)
                    
                    sources = [{"page": doc.metadata.get("page", "?"), "content": doc.page_content} for doc, score in result["retrieved_chunks"]]
                    st.markdown(result["answer"])
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result["answer"],
                        "sources": sources
                    })
                    
                    with st.expander("View Institutional Sources"):
                        for src in sources:
                            st.markdown(f"<div class='source-box'><b>Page {src['page']}</b><br>{src['content']}</div>", unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Bottom Footer
st.markdown("<p style='text-align: center; color: #414754; font-size: 0.65rem; margin-top: 30px; font-weight: 800; letter-spacing: 1px;'>MODEL: RAG INSTITUTIONAL V4.2 • CONTEXT WINDOW: 128K TOKENS</p>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Populate Sidebar History Container
# ──────────────────────────────────────────────
with history_container:
    has_history = False
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            has_history = True
            short_msg = msg["content"][:28] + "..." if len(msg["content"]) > 28 else msg["content"]
            st.markdown(f"<p style='color: #8b90a0; font-size: 0.85rem; cursor: pointer; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>💬 {short_msg}</p>", unsafe_allow_html=True)
            
    if not has_history:
        st.markdown("<p style='color: #414754; font-size: 0.8rem; font-style: italic;'>No recent inquiries.</p>", unsafe_allow_html=True)
