from app.services.embedding_generation.ensure_embed import ensure_embeddings
from app.services.vector_db.build_vector_store import build_medical_vector_store
from app.utils.fingerprint import compute_fingerprint
from app.config.config import RAGConfig
from app.utils.loggers import get_logger
from app.utils.exceptions import BuildKnowledgeBaseError

logger = get_logger(__name__)

''' compute fingerprint and generate embeddings if needed'''
def create_vectors(config: RAGConfig):
    try:

        # Compute fingerprint
        fingerprint = compute_fingerprint(config)

        # Build / reuse embeddings
        ensure_embeddings(lambda: build_medical_vector_store(config), fingerprint, config)

    except Exception as bkbe:
        logger.error(f"Error building medical vector store: {bkbe}") 
        raise BuildKnowledgeBaseError(f"Failed to build medical vector store: {bkbe}")
    
    logger.info("Medical vector store built successfully.")   