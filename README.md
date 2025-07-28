
# 🧠 RAG Chatbot App with PDF, DOCX & Excel Support

This is a **Retrieval-Augmented Generation (RAG) Chatbot App** built using **Streamlit**, **FastAPI**, and **Qdrant**.  
The app allows you to upload documents (PDF, DOCX, Excel), ask questions based on their content, and receive intelligent responses powered by **local** or **OpenAI LLMs**.

![RAG Chatbot Screenshot](screenshot.png) <!-- Replace with actual image filename -->

---

## 🚀 Features

- 🔍 Ask questions directly based on uploaded documents  
- 📄 Supports PDF, Word, and Excel file formats  
- 🧠 Integrates local (Ollama) and OpenAI-based LLMs  
- 🔎 Uses Qdrant for fast and accurate semantic search  
- ⚡ Real-time responses using Streamlit UI  
- 🧾 Answers are contextually enriched using top-matching chunks  

---

## 🛠️ How to Run Locally

Follow the steps below to set up and run the RAG Chatbot on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv rag_env
```

Activate the virtual environment:

**For Windows:**
```bash
rag_env\Scripts\activate
```

**For Mac/Linux:**
```bash
source rag_env/bin/activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

Ensure you have Streamlit and FastAPI installed:

```bash
pip install streamlit fastapi
```

### 4. Start Qdrant (Vector Database)

> You must have Docker installed.

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 5. (Optional) Set OpenAI API Key

If you want to use OpenAI models instead of the local LLM:

```bash
export OPENAI_API_KEY=your_openai_key  # Windows: set OPENAI_API_KEY=your_openai_key
```

### 6. Start the Backend Server

```bash
uvicorn main:app --reload --port 8000
```

### 7. Launch the Frontend (Streamlit)

```bash
streamlit run app.py
```

### 8. Interact with the App

- Visit [http://localhost:8501](http://localhost:8501)  
- Use the sidebar to upload a document (PDF, DOCX, Excel)  
- Switch to the **“Ask Question”** tab  
- Select your preferred LLM provider (local / OpenAI)  
- Ask any question based on the uploaded content  

---

## 🔧 Required Libraries

- `streamlit` – For interactive frontend  
- `fastapi` – Backend API  
- `sentence-transformers` – For generating text embeddings  
- `qdrant-client` – To store and search vector embeddings  
- `langchain` – For prompt chaining and LLM integration  
- `uvicorn` – ASGI server for FastAPI  
- `python-docx`, `PyMuPDF`, `pandas`, `openpyxl`, `xlrd` – For text extraction  

👉 Everything is listed in the `requirements.txt` file.

---

## ✨ How It Works

The RAG Chatbot follows this intelligent pipeline:

1. **Upload File** – Choose a document (PDF, DOCX, or Excel)  
2. **Text Extraction** – Extract raw text using custom extractors  
3. **Chunking** – Break text into small overlapping segments  
4. **Embedding** – Convert chunks into vector embeddings using `MiniLM`  
5. **Storage** – Save vectors to Qdrant for similarity search  
6. **Query Handling** – Your question is embedded and matched with top chunks  
7. **LLM Response** – A final answer is generated using an LLM (via LangChain)

---

## 📁 File Structure

```
├── app.py                 # Streamlit UI
├── main.py                # FastAPI backend
├── embedder.py            # Embedding logic using SentenceTransformer
├── llm_chain.py           # LangChain integration with local/OpenAI LLM
├── qdrant_handler.py      # Qdrant database operations
├── text_extractor.py      # Extract text from PDF, Word, Excel
├── utils.py               # Text chunking utilities
├── requirements.txt       # All dependencies
├── README.md              # This documentation file
└── screenshot.png         # UI screenshot (optional)
```

---

## 🔧 Future Improvements

- ⬆️ Allow multiple document uploads and chat history  
- 🌐 Deploy publicly on Streamlit Cloud or Hugging Face Spaces  
- 🔁 Add support for TXT and CSV formats  
- 📡 Integrate with real-time document sources (Google Drive, Dropbox, etc.)

---

## 🙋‍♂️ Want to Contribute?

Feel free to fork this repository, suggest improvements, or create pull requests.  
**Contributions are always welcome!**

---

## 📬 Contact

- 📧 priyanshu.nayak.555@gmail.com
---
