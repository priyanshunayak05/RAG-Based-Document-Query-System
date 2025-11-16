# api.py
# This is your main FastAPI server file.

import uvicorn
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List

# Import your own project modules
import text_extractor
import embedder
import qdrant_handler
import llm_chain

# --- Application Setup ---
app = FastAPI(
    title="RAG Chatbot Backend",
    description="API for uploading files and querying a RAG model.",
)

# --- Pydantic Models ---
class UploadResponse(BaseModel):
    file_id: str
    message: str

class QueryRequest(BaseModel):
    query: str
    provider: str = "local"

# --- RAG Helper Function ---
def build_rag_prompt(query: str, context_chunks: List[str]) -> str:
    """Helper function to build the final prompt for the LLM."""
    context = "\n\n---\n\n".join(context_chunks)
    
    template = f"""
    You are a helpful assistant. Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know. Do not try to make up an answer.

    Context:
    {context}

    Question:
    {query}

    Helpful Answer:
    """
    return template

# --- API Endpoints ---

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file, extract text, embed it, and store in Qdrant.
    """
    try:
        file_bytes = await file.read()
        file_id = file.filename  # Use filename as a simple ID
        
        # 1. Extract Text
        print(f"Extracting text from {file_id}...")
        text_content = text_extractor.extract_text(file_bytes, file_id)
        # Simple chunking (you can replace with a real text splitter)
        chunks = [text_content[i:i+1000] for i in range(0, len(text_content), 1000)]
        
        # 2. Embed Chunks
        print(f"Embedding {len(chunks)} chunks...")
        vectors = embedder.embed_texts(chunks)
        
        # 3. Store in Qdrant
        print("Storing vectors in Qdrant...")
        qdrant_handler.store_chunks(chunks, vectors, file_id)
        
        return UploadResponse(file_id=file_id, message="File uploaded and indexed successfully.")
    
    except Exception as e:
        print(f"Error during upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search_rag")
async def search_rag(query: str, provider: str = "local"):
    """
    Endpoint to search Qdrant, build a prompt, and stream the LLM response.
    """
    try:
        # 1. Embed the query
        print(f"Embedding query: {query}")
        query_vector = embedder.embed_query(query)
        
        # 2. Search Qdrant for relevant chunks
        print("Searching Qdrant for context...")
        search_results = qdrant_handler.search_chunks(query_vector, top_k=3)
        context_chunks = [point.payload['chunk'] for point in search_results]
        
        if not context_chunks:
            print("No context found.")
            async def no_context_stream():
                yield "I could not find any relevant information in the uploaded documents to answer your question."
            return StreamingResponse(no_context_stream(), media_type="text/plain")

        # 3. Build the RAG prompt
        prompt = build_rag_prompt(query, context_chunks)
        
        # 4. Stream the response from the LLM
        print("Streaming LLM response...")
        return StreamingResponse(
            llm_chain.stream_llm(prompt, provider=provider), 
            media_type="text/plain"
        )
        
    except Exception as e:
        print(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
def on_startup():
    """
    Initialize Qdrant collection on server startup.
    """
    print("Initializing Qdrant...")
    qdrant_handler.init_qdrant() # Uses the vector size from embedder
    print("Qdrant initialized.")

# --- Main execution ---
if __name__ == "__main__":
    """
    Allows running the server locally for testing.
    Run with: python api.py
    """
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
