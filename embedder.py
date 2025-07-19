"""
embedder.py

This module provides functions to convert text data into vector embeddings
using a pre-trained SentenceTransformer model. These embeddings are used
for semantic search and retrieval in the RAG system.

Functions:
    embed_texts(chunks): Embeds a list of text chunks into vectors.
    embed_query(text): Embeds a single query string into a vector.
"""
from sentence_transformers import SentenceTransformer

#  this model converts text  # into 384-dimensional vector embeddings

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(chunks):
    """
    Embed a list of text chunks into vector representations.

    Args:
        chunks (List[str]): List of text strings to embed.

    Returns:
        np.ndarray: Array of vector embeddings for the input chunks.
    """
    return model.encode(chunks)
    
def embed_query(text):
    """
    Embed a single query string into a vector representation.

    Args:
        text (str): The query string to embed.

    Returns:
        np.ndarray: Vector embedding for the input query.
    """
    return model.encode([text])[0]
