"""
RAG Functions - Public functions for AI agents to interact with ChromaDB

This module provides a clean public API for AI agents to:
- Connect to ChromaDB
- Query collections
- Create embeddings and store documents in ChromaDB with collection names

This module reuses functions from rag.py to avoid code duplication.

Usage:
    from rag_functions import get_rag_connection, create_embeddings_and_store, sample_query
    
    # Get RAG connection (returns chroma_db_context)
    chroma_db = get_rag_connection(collection_name="my_collection")
    
    # Query the collection using chroma_db_context
    results = chroma_db.query("What is ROE?", collection="my_collection")
    
    # Create embeddings and store documents
    create_embeddings_and_store(
        texts=["Document 1 text", "Document 2 text"],
        collection_name="my_collection",
        metadatas=[{"source": "doc1"}, {"source": "doc2"}]
    
    
    # Sample query
    results = sample_query("What is ROE?", collection_name="my_collection")
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np

# Import reusable functions from rag.py
# Note: We need to import rag as a module to avoid circular imports
# and to ensure environment variables are loaded
import sys
sys.path.insert(0, str(Path(__file__).parent))

# Import from rag.py - this will load environment variables and initialize everything
# Note: These functions are now public in rag.py (no underscore prefix)
from rag import (
    get_chromadb_client,
    get_embedder,
    normalize_query,
    CHROMADB_HOST,
    CHROMADB_PORT,
    CHROMADB_AUTH_TOKEN,
    EMBEDDING_MODEL,
    VECTOR_COLLECTION,
    EMBED_BATCH,
)

# Set default collection from environment
DEFAULT_COLLECTION = VECTOR_COLLECTION


class ChromaDBContext:
    """Context object for querying ChromaDB collections.
    
    Provides a clean interface for querying ChromaDB collections.
    The query method can query any collection, not just the one used for initialization.
    
    Attributes:
        client: ChromaDB HTTP client
        default_collection: Default collection name (used if collection not specified in query)
    """
    
    def __init__(self, default_collection: Optional[str] = None):
        """Initialize ChromaDB context.
        
        Args:
            default_collection: Default collection name (optional)
        """
        self.client = get_chromadb_client()
        self.default_collection = default_collection or DEFAULT_COLLECTION
    
    def query(self, query_string: str, collection: Optional[str] = None, k: int = 4) -> List[Dict[str, Any]]:
        """Query a ChromaDB collection.
        
        Args:
            query_string: Query text to search for
            collection: Collection name to query (optional, uses default if not specified)
            k: Number of results to return (default: 4)
            
        Returns:
            List of dictionaries containing:
            - document: Document text
            - metadata: Document metadata
            - distance: Similarity distance
            - id: Document ID
            
        Example:
            results = chroma_db.query("What is ROE?", collection="financial_terms")
            for result in results:
                print(result["document"])
        """
        if not isinstance(query_string, str) or not query_string.strip():
            return []
        
        # Use specified collection or default
        collection_name = collection or self.default_collection
        
        # Normalize query using function from rag.py
        q_normalized = normalize_query(query_string)
        if not q_normalized:
            return []
        
        # Get collection
        try:
            coll = self.client.get_or_create_collection(name=collection_name)
        except Exception as e:
            raise ValueError(f"Failed to get collection '{collection_name}': {e}")
        
        # Create query embedding using get_embedder() from rag.py
        embedder = get_embedder()
        q_vec = next(embedder.query_embed(q_normalized))
        
        # Ensure q_vec is a flat list of floats
        if hasattr(q_vec, "tolist"):
            q_vec = q_vec.tolist()
        elif not isinstance(q_vec, list):
            q_vec = list(q_vec)
        
        # Flatten if nested
        if isinstance(q_vec, list) and len(q_vec) > 0:
            if isinstance(q_vec[0], list):
                q_vec = q_vec[0] if len(q_vec) == 1 else [item for sublist in q_vec for item in sublist]
        
        # Final check: ensure q_vec is a flat list of numbers
        if isinstance(q_vec, list) and len(q_vec) > 0:
            if not isinstance(q_vec[0], (int, float)) and isinstance(q_vec[0], (list, np.ndarray)):
                q_vec = q_vec[0]
                if hasattr(q_vec, "tolist"):
                    q_vec = q_vec.tolist()
        
        # Convert to numpy array for ChromaDB
        if isinstance(q_vec, list):
            q_vec = np.array(q_vec, dtype=np.float32)
        
        # Validate k
        k = max(1, min(int(k), 50))
        
        # Query ChromaDB
        try:
            res = coll.query(
                query_embeddings=[q_vec],
                n_results=k,
                include=["documents", "metadatas", "distances", "ids"]
            )
        except Exception as e:
            raise RuntimeError(f"Failed to query collection '{collection_name}': {e}")
        
        # Extract results
        ids_list = res.get("ids", [[]])
        docs_list = res.get("documents", [[]])
        metas_list = res.get("metadatas", [[]])
        dists_list = res.get("distances", [[]])
        
        # Extract first (and only) result list
        ids = ids_list[0] if isinstance(ids_list, list) and len(ids_list) > 0 else []
        docs = docs_list[0] if isinstance(docs_list, list) and len(docs_list) > 0 else []
        metas = metas_list[0] if isinstance(metas_list, list) and len(metas_list) > 0 else []
        dists = dists_list[0] if isinstance(dists_list, list) and len(dists_list) > 0 else []
        
        # Format results
        results = []
        for doc_id, text, md, dist in zip(ids, docs, metas, dists):
            try:
                distance = float(dist) if dist is not None else 0.0
            except (ValueError, TypeError):
                distance = 0.0
            
            results.append({
                "id": doc_id,
                "document": text,
                "metadata": md or {},
                "distance": distance
            })
        
        return results


def get_rag_connection(collection_name: Optional[str] = None) -> ChromaDBContext:
    """RAG Connectivity function - Returns chroma_db_context.
    
    This function provides RAG connectivity and returns a chroma_db_context
    that can be used to query ChromaDB collections.
    
    Args:
        collection_name: Optional default collection name (uses VECTOR_COLLECTION env var if not specified)
        
    Returns:
        ChromaDBContext instance (chroma_db_context)
        
    Example:
        # Get RAG connection
        chroma_db = get_rag_connection()
        
        # Query using chroma_db_context
        results = chroma_db.query("What is ROE?", collection="financial_terms")
    """
    return ChromaDBContext(default_collection=collection_name)


def create_embeddings_and_store(
    texts: List[str],
    collection_name: str,
    metadatas: Optional[List[Dict[str, Any]]] = None,
    ids: Optional[List[str]] = None,
    batch_size: int = None
) -> Dict[str, Any]:
    """Create embeddings for texts and store them in ChromaDB.
    
    This function uses semantic chunking (via FastEmbed) to create embeddings
    and stores them in the specified ChromaDB collection.
    Reuses embedding creation functions from rag.py.
    
    Args:
        texts: List of text documents to embed and store
        collection_name: Name of the ChromaDB collection to store in
        metadatas: Optional list of metadata dictionaries (one per text)
        ids: Optional list of document IDs (one per text)
        batch_size: Batch size for embedding creation (defaults to EMBED_BATCH from rag.py)
        
    Returns:
        Dictionary containing:
        - stored: Number of documents stored
        - collection: Collection name
        - embedding_model: Embedding model used
        
    Example:
        # Store documents with metadata
        result = create_embeddings_and_store(
            texts=["ROE is Return on Equity", "PE is Price to Earnings"],
            collection_name="financial_terms",
            metadatas=[{"source": "doc1"}, {"source": "doc2"}],
            ids=["doc1", "doc2"]
        )
        print(f"Stored {result['stored']} documents")
    """
    if not texts:
        return {"stored": 0, "collection": collection_name, "embedding_model": EMBEDDING_MODEL}
    
    # Get ChromaDB client and collection (reuses function from rag.py)
    client = get_chromadb_client()
    coll = client.get_or_create_collection(name=collection_name)
    
    # Prepare metadata and IDs
    if metadatas is None:
        metadatas = [{}] * len(texts)
    elif len(metadatas) != len(texts):
        raise ValueError(f"metadatas length ({len(metadatas)}) must match texts length ({len(texts)})")
    
    if ids is None:
        import uuid
        ids = [str(uuid.uuid4()) for _ in texts]
    elif len(ids) != len(texts):
        raise ValueError(f"ids length ({len(ids)}) must match texts length ({len(texts)})")
    
    # Use batch_size from rag.py if not specified
    if batch_size is None:
        batch_size = EMBED_BATCH
    
    # Get embedder from rag.py
    embedder = get_embedder()
    
    # Create embeddings in batches
    stored_count = 0
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_metas = metadatas[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        
        try:
            # Create embeddings for batch using get_embedder() from rag.py
            embeddings = list(embedder.embed(batch_texts, batch_size=batch_size))
            
            # Convert to list of lists
            embedding_list = []
            for emb in embeddings:
                if hasattr(emb, "tolist"):
                    embedding_list.append(emb.tolist())
                elif isinstance(emb, list):
                    embedding_list.append(emb)
                else:
                    embedding_list.append(list(emb))
            
            # Upsert to ChromaDB (updates if exists, adds if new)
            coll.upsert(
                ids=batch_ids,
                embeddings=embedding_list,
                documents=batch_texts,
                metadatas=batch_metas
            )
            
            stored_count += len(batch_texts)
            
        except Exception as e:
            raise RuntimeError(f"Failed to store batch starting at index {i}: {e}")
    
    return {
        "stored": stored_count,
        "collection": collection_name,
        "embedding_model": EMBEDDING_MODEL
    }


# Sample query function for demonstration
def sample_query(query_string: str, collection_name: Optional[str] = None, k: int = 4) -> List[Dict[str, Any]]:
    """Sample query function for querying ChromaDB.
    
    This is a convenience function that creates a ChromaDB context and queries it.
    
    Args:
        query_string: Query text to search for
        collection_name: Collection name to query (optional)
        k: Number of results to return (default: 4)
        
    Returns:
        List of query results
        
    Example:
        results = sample_query("What is ROE?", collection_name="financial_terms")
        for result in results:
            print(f"Document: {result['document']}")
            print(f"Distance: {result['distance']}")
    """
    chroma_db = get_rag_connection(collection_name=collection_name)
    return chroma_db.query(query_string, collection=collection_name, k=k)


# Main entry point for testing
if __name__ == "__main__":
    # Example usage
    print("RAG Functions - Example Usage")
    print("=" * 50)
    
    # Get RAG connection
    print("\n1. Getting RAG connection...")
    chroma_db = get_rag_connection()
    
    # Sample query
    print("\n2. Running sample query...")
    try:
        results = sample_query("What is ROE?", k=2)
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"  Document: {result['document'][:100]}...")
            print(f"  Distance: {result['distance']:.4f}")
    except Exception as e:
        print(f"Error querying: {e}")
    
    print("\n" + "=" * 50)
    print("Example usage complete!")

