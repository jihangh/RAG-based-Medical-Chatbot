from app.utils.loggers import get_logger
from app.utils.state_loader import load_state, save_state
from app.config.config import RAGConfig

logger= get_logger(__name__)

''' check if vectors exist in vector store'''

def get_vector_count(config: RAGConfig) -> int:
    try:
        index = config.pinecone_vector_client.Index(config.index_name)
        stats = index.describe_index_stats()
        return stats["namespaces"].get(config.name_space, {}).get("vector_count", 0)
    except Exception as e:
        logger.warning(f"Pinecone error: {e}")
        return 0


def vectorstore_exists(config: RAGConfig) -> bool:
    return get_vector_count(config) > 0



''' check if no embeddings were created or 
    if  fingerprint changed then generate embeddings,
    else use existing embeddings '''

def ensure_embeddings(create_embeddings_fn, fingerprint: str, config: RAGConfig):
    state = load_state() 
    pinecone_count = get_vector_count(config)

    # No state
    if not state.get("fingerprint"):
        logger.info("No state found. Creating embeddings...")

        create_embeddings_fn()
        pinecone_count = get_vector_count(config)
        state["fingerprint"] = fingerprint
        state["vector_count"] = pinecone_count
        save_state(state)
        return

    # Fingerprint changed
    if state["fingerprint"] != fingerprint:
    
        logger.info("Fingerprint changed. Rebuilding embeddings...")

        create_embeddings_fn()
        pinecone_count = get_vector_count(config)
        state["fingerprint"] = fingerprint
        state["vector_count"] = pinecone_count
        save_state(state)
        return

    # Vectorstore missing
    if pinecone_count == 0:

        logger.info("No records in vector store. Rebuilding embeddings...")
        create_embeddings_fn()
        pinecone_count = get_vector_count(config)
        state["vector_count"] = pinecone_count
        save_state(state)
        return

    # Drift detection 
    if pinecone_count != state.get("vector_count"):
        logger.info("Vector count drift detected. Updating state.")
        state["vector_count"] = pinecone_count
        save_state(state)

    logger.info("Using existing embeddings")

