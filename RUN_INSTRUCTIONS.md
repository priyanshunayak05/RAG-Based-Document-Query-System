# How to Run the RAG Chatbot Locally

This guide will help you run the RAG Chatbot project on your local machine without any external assistance.

## Prerequisites

1.  **Python 3.10+**: Ensure Python is installed.
2.  **Ollama**: Download and install [Ollama](https://ollama.com/).
    *   Ensure Ollama is running (`ollama serve` in a terminal, or just start the app).
    *   Pull the required model: `ollama pull llama3.2:1b`

## Setup

1.  **Navigate to the project directory**:
    ```powershell
    cd path\to\rag_project
    ```

2.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    pip install streamlit langchain-text-splitters langchain-core langchain-ollama
    ```

## Running the Application

You need to run **two** separate terminals.

### Terminal 1: Backend Server (FastAPI)

Run the following command to start the backend API:

```powershell
uvicorn main:app --reload --port 8000
```

*   You should see `Uvicorn running on http://127.0.0.1:8000`.
*   Keep this terminal open.

### Terminal 2: Frontend (Streamlit)

Open a **new** terminal window, navigate to the project folder, and run:

```powershell
streamlit run app.py
```

*   This will automatically open your browser to `http://localhost:8501`.
*   You can now upload files and chat with them!

## Troubleshooting

*   **Connection Refused**: Make sure the Backend Server (Terminal 1) is running before you try to upload files in the Frontend.
*   **Memory Errors**: If you see "model requires more system memory", ensure you are using the `llama3.2:1b` model (configured in `llm_chain.py`) and not a larger one.
*   **Ollama Error**: Ensure the Ollama application is running in the background.
