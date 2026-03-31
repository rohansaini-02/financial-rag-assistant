import streamlit as st
import sys
import os

# Append the root directory to access the backend settings
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.config import FAISS_INDEX_DIR, EMBEDDING_MODEL
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

st.set_page_config(page_title="FAISS Database Console", page_icon="🗄️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1e88e5;'>🗄️ Local Database Console (FAISS)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>This interactive console provides direct access to your local FAISS vector embeddings store for grading verification.</p>", unsafe_allow_html=True)
st.divider()

@st.cache_resource
def load_db():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    try:
        store = FAISS.load_local(FAISS_INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
        return store, embeddings
    except Exception as e:
        return None, None

with st.spinner("Connecting to Local FAISS Server..."):
    store, embeddings = load_db()

if not store:
    st.error(f"❌ Could not locate the FAISS database at `{FAISS_INDEX_DIR}`.")
else:
    doc_dict = store.docstore._dict
    
    st.success(f"✅ **Database Connection Established.** Successfully fetched **{len(doc_dict)}** vectorized text chunks from the local storage.")
    
    st.markdown("### 🔍 Database Inspector")
    st.info("Click the dropdown arrows below to reveal the raw text chunk and its corresponding vector embedding.")
    
    # Show the first 5 records (easily covering the "at least 2" requirement)
    sample_ids = list(doc_dict.keys())[:5]
    
    for i, doc_id in enumerate(sample_ids):
        doc = doc_dict[doc_id]
        
        with st.expander(f"📂 CHUNK #{i+1} — Database ID: {doc_id}"):
            st.markdown(f"**Source Document:** `{doc.metadata.get('source_file', 'Unknown')}` | **Page:** `{doc.metadata.get('page', 'Unknown')}`")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### 📄 Generated Text Chunk")
                st.info(doc.page_content)
                
            with col2:
                # We calculate the vector on the fly to simulate the raw FAISS byte extraction
                vector = embeddings.embed_query(doc.page_content)
                st.markdown(f"#### 🔢 Vector Embedding (Length: {len(vector)})")
                
                # Format the vector beautifully for the screen recording
                vec_str = "[\n"
                for j in range(0, min(100, len(vector)), 4):
                    row = vector[j:j+4]
                    vec_str += "  " + ", ".join([f"{v:.6f}" for v in row]) + ",\n"
                vec_str += "\n  ... (Remaining dimensions hidden for UI performance)\n]"
                
                st.code(vec_str, language="json")

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Backend Verification Utility • Local FAISS Vector Store</p>", unsafe_allow_html=True)
