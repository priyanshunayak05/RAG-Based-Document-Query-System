import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

qdrant = QdrantClient(host="localhost", port=6333)
COLLECTION = "rag_files"

def init_qdrant():
    global client
    client = QdrantClient(
        url="https://52adf401-d449-433f-8d8a-676652579db5.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ccW1CDyRZEE00IDEFnx0iFOx1p0wEfgMcUAgOYiPZK0",                       # <-- Replace with your Qdrant API key
    )

    # Create collection if it doesn’t exist
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # 384 = embedding size (SentenceTransformers)
    )

def store_chunks(chunks, vectors, file_id):
    points = [
        PointStruct(
            id=int(uuid.uuid4().int >> 64),
            vector=vec.tolist(),
            payload={ "file_id": file_id, "chunk": chunk }
        )
        for vec, chunk in zip(vectors, chunks)
    ]
    qdrant.upsert(collection_name=COLLECTION, points=points)

def search_chunks(query_vector, top_k=5):
    result = qdrant.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=top_k
    )
    return result
