import streamlit as st
import requests

st.title("🧠 RAG Chatbot with Local LLM")

# API_BASE = "http://localhost:8000"
API_BASE ="https://my-rag-backend.onrender.com" # Adjust if backend runs on a different port

# Sidebar selection
option = st.sidebar.selectbox("Choose Action", ["Upload File", "Ask Question"])
provider = st.sidebar.radio("Select LLM Provider", ["local", "openai"])

if option == "Upload File":
    uploaded_file = st.file_uploader("Upload a PDF, DOCX, or Excel file", type=["pdf", "docx", "xlsx", "xls"])
    if uploaded_file and st.button("Upload"):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(f"{API_BASE}/upload", files=files)
        if response.status_code == 200:
            try:
                file_id = response.json().get('file_id')
                st.success(f"File uploaded and indexed. File ID: {file_id}")
            except Exception:
                st.success("File uploaded and indexed.")
        else:
            try:
                error_msg = response.json().get('error')
            except Exception:
                error_msg = response.text
            st.error(f"❌ Upload failed: {error_msg}")


elif option == "Ask Question":
    query = st.text_input("Enter your question")
    if query and st.button("Ask"):
        params = {"query": query, "provider": provider}
        response = requests.get(f"{API_BASE}/search_rag", params=params, stream=True)
        if response.status_code == 200:
            st.markdown("### 💬 Answer")
            answer_placeholder = st.empty()
            answer = ""
            for chunk in response.iter_content(chunk_size=32, decode_unicode=True):
                answer += chunk
                answer_placeholder.write(answer)
        else:
            try:
                error_msg = response.json().get('error')
            except Exception:
                error_msg = response.text
            st.error(f"Failed to retrieve response: {error_msg}")
