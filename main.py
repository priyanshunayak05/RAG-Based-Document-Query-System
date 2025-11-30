from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
import uuid

from text_extractor import extract_text
from utils import chunk_text
from embedder import embed_texts, embed_query
from qdrant_handler import init_qdrant, store_chunks, search_chunks
from llm_chain import run_llm, stream_llm# <-- Only this import

from fastapi.responses import StreamingResponse

app = FastAPI()
init_qdrant()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_id = str(uuid.uuid4())
    try:
        text = extract_text(file_bytes, file.filename)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    
    # Detect filetype for chunking
    if file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
        filetype = "excel"
    elif file.filename.endswith(".pdf"):
        filetype = "pdf"
    else:
        filetype = None

    chunks = chunk_text(text, max_length=430, overlap=30,filetype=filetype)
    vectors = embed_texts(chunks)
    store_chunks(chunks, vectors, file_id)
    return {"message": "File indexed", "file_id": file_id, "chunks": len(chunks)}


@app.get("/search_rag")
def search_with_rag(query: str = Query(...), provider: str = "local"):
    try:
        vector = embed_query(query)
        results = list(search_chunks(vector))

        if not results:
            def gen():
                yield "No relevant documents found."
            return StreamingResponse(gen(), media_type="text/plain")

        context = "\n".join([r.payload["chunk"] for r in results])
        prompt = f"Use the following context to answer the question:\n{context}\n\nQuestion: {query}"

        def gen():
            try:
                for chunk in stream_llm(prompt, provider=provider):
                    yield chunk
            except Exception as e:
                yield f"\n[Error: {str(e)}]"
        return StreamingResponse(gen(), media_type="text/plain")
    except Exception as e:
        def gen():
            yield f"Error: {str(e)}"
        return StreamingResponse(gen(), media_type="text/plain")