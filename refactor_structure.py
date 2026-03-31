import os
import shutil
import glob

# Ensure we're in the right directory
os.chdir(r"d:\SEMESTERS DATA\SEM 4\RAG Assignment")

# 1. Create Structure
os.makedirs("frontend", exist_ok=True)
os.makedirs("backend", exist_ok=True)
os.makedirs("tests", exist_ok=True)
with open("backend/__init__.py", "w") as f: f.write("")
with open("frontend/__init__.py", "w") as f: f.write("")
with open("tests/__init__.py", "w") as f: f.write("")

# 2. Move Files
files_to_backend = [
    "config.py", "embedding_store.py", "llm_handler.py", 
    "pdf_loader.py", "rag_pipeline.py", "retriever.py", "text_chunker.py"
]
for f in files_to_backend:
    if os.path.exists(f): 
        shutil.move(f, os.path.join("backend", f))

if os.path.exists("streamlit_app.py"):
    shutil.move("streamlit_app.py", os.path.join("frontend", "streamlit_app.py"))

for f in glob.glob("test_*.py"):
    if os.path.exists(f):
        shutil.move(f, os.path.join("tests", f))

# 3. Modify backend files to use absolute imports from 'backend'
backend_modules = [m.replace(".py", "") for m in files_to_backend]

for bf in files_to_backend:
    path = os.path.join("backend", bf)
    if not os.path.exists(path): continue
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        
    # Replace simple imports
    for mod in backend_modules:
        content = content.replace(f"import {mod}\n", f"from backend import {mod}\n")
        content = content.replace(f"from {mod} import", f"from backend.{mod} import")
        
    # Specific fix for config.py dot env loading
    if bf == "config.py":
        new_config = []
        for line in content.splitlines():
            if "load_dotenv()" in line:
                new_config.append('ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))')
                new_config.append('load_dotenv(os.path.join(ROOT_DIR, ".env"))')
            else:
                new_config.append(line)
        content = "\n".join(new_config)
            
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

# 4. Modify frontend/streamlit_app.py
st_path = os.path.join("frontend", "streamlit_app.py")
if os.path.exists(st_path):
    with open(st_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Needs sys path injection BEFORE importing from backend
    injection = """import sys\nimport os\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))\n"""
    
    content = content.replace("from rag_pipeline import RAGPipeline", injection + "from backend.rag_pipeline import RAGPipeline")
    
    with open(st_path, "w", encoding="utf-8") as file:
        file.write(content)

# 5. Modify tests pathing
for tf in glob.glob("tests/test_*.py"):
    with open(tf, "r", encoding="utf-8") as file:
        content = file.read()
    
    injection = """import sys\nimport os\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))\n"""
    if "import sys" not in content:
        content = injection + content
        
    for mod in backend_modules:
        content = content.replace(f"from {mod} import", f"from backend.{mod} import")
        content = content.replace(f"import {mod}\n", f"from backend import {mod}\n")
        
    with open(tf, "w", encoding="utf-8") as file:
        file.write(content)

# 6. Modify main.py pathing (root CLI tool)
if os.path.exists("main.py"):
    with open("main.py", "r", encoding="utf-8") as file:
        content = file.read()
    
    for mod in backend_modules:
        content = content.replace(f"from {mod} import", f"from backend.{mod} import")
    
    with open("main.py", "w", encoding="utf-8") as file:
        file.write(content)

# 7. Update README to show new run instruction
readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()
    content = content.replace("streamlit run streamlit_app.py", "streamlit run frontend/streamlit_app.py")
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(content)

print("Refactoring complete.")
