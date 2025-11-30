import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

qdrant = QdrantClient(":memory:")
COLLECTION = "rag_files"

def init_qdrant():
    if not qdrant.collection_exists(COLLECTION):
        qdrant.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
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
