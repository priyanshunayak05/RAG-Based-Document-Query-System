import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# ----------------------------
# Configuration
# ----------------------------
COLLECTION = "rag_files"

# Connect to Qdrant (Cloud or local)
qdrant = QdrantClient(
    url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
    api_key=os.environ.get("QDRANT_API_KEY")  # None if using local Qdrant
)

# ----------------------------
# Initialize collection
# ----------------------------
def init_qdrant(vector_size: int = 384):
    """
    Create or recreate collection if it does not exist.
    vector_size: dimension of embeddings (e.g., 384 for sentence-transformers)
    """
    if not qdrant.collection_exists(COLLECTION):
        qdrant.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        print(f"Collection '{COLLECTION}' created with size={vector_size}.")
    else:
        print(f"Collection '{COLLECTION}' already exists.")

# ----------------------------
# Store chunks with embeddings
# ----------------------------
def store_chunks(chunks, vectors, file_id):
    """
    Store document chunks with corresponding vectors in Qdrant.
    chunks: list of text chunks
    vectors: list of embeddings (numpy array or list)
    file_id: identifier for the document
    """
    points = [
        PointStruct(
            id=int(uuid.uuid4().int >> 64),
            vector=vec.tolist() if hasattr(vec, "tolist") else vec,
            payload={"file_id": file_id, "chunk": chunk}
        )
        for vec, chunk in zip(vectors, chunks)
    ]

    try:
        qdrant.upsert(collection_name=COLLECTION, points=points)
        print(f"Inserted {len(points)} points into '{COLLECTION}'.")
    except Exception as e:
        print("Error storing chunks:", e)

# ----------------------------
# Search nearest chunks
# ----------------------------
def search_chunks(query_vector, top_k=5, file_id=None):
    """
    Search top_k nearest neighbors for a query vector.
    Optionally filter by file_id.
    Returns list of matching points.
    """
    filter_payload = {"must": [{"key": "file_id", "match": {"value": file_id}}]} if file_id else None

    try:
        results = qdrant.search(
            collection_name=COLLECTION,
            query_vector=query_vector,
            limit=top_k,
            filter=filter_payload
        )
        return results
    except Exception as e:
        print("Search error:", e)
        return []

# ----------------------------
# Utility: List all collections
# ----------------------------
def list_collections():
    try:
        return qdrant.get_collections()
    except Exception as e:
        print("Error listing collections:", e)
        return []
