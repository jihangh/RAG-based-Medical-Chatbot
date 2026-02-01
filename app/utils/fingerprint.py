import json
import hashlib
from app.config.config import RAGConfig




# def compute_doc_hash(docs):
#     """Compute hash based on chunk text content."""
#     sha = hashlib.sha256()
#     for d in docs:
#         sha.update(d.page_content.strip().encode("utf-8"))
#     return sha.hexdigest()



def compute_fingerprint(config: RAGConfig) -> str:
    ''' compute a fingerprint'''
    
    fingerprint_payload = {
        # you can add doc_hash here  but it will add latency ("doc_hash": doc_hash)
        # since we need to load and process pdf on every run
        "vector-client": config.pinecone_vector_client.__class__.__name__,
        "embedding_client": config.openai_client.__class__.__name__ ,
        "dimension": config.dim,
        "dense_model": config.dense_model,
        "chunk_size": config.chunk_size,
        "chunk_overlap": config.chunk_overlap,
        "index": config.index_name,
        "namespace": config.name_space,
    }
    serialized = json.dumps(fingerprint_payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()