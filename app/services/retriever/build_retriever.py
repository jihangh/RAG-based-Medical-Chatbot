from app.services.retriever.hybrid_retriever import HybridRetriever
from app.services.embedding_generation.query_embeddings import generate_query_embeddings
from app.utils.loggers import get_logger
from app.utils.exceptions import HybridRetreiverError

logger = get_logger(__name__)


def retrieve_docs(
    pinecone_vector_client,
    index_name: str,
    name_space: str,
    openai_client,
    dense_model: str,
    dim: int,
    query: str,
    top_ret_doc: int,
    alpha: float
):
    """Retrieve documents from Pinecone index using hybrid retrieval."""
    try:

        #generate query embeddings
        dense_query_embedding, sparse_query_embedding = generate_query_embeddings(query, 
                                                                                dense_model, 
                                                                                dim, 
                                                                                openai_client, 
                                                                                pinecone_vector_client)
        """Perform hybrid search on Pinecone index using dense and sparse query embeddings."""
        # Initialize HybridRetriever
        hybrid_retriever = HybridRetriever(pinecone_vector_client, 
                                        index_name, 
                                        name_space)
        #retrieve similar documents from Pinecone based on hybrid retrieval
        
        query_response= hybrid_retriever.contextual_hybrid_search(
                                dense_query_embedding, 
                                sparse_query_embedding,
                                top_ret_doc, 
                                alpha)
        #get the content of the most similar retrieved documents
        num_docs = min(top_ret_doc, len(query_response.matches))
        retrieved_docs = [query_response.matches[i].metadata['text'] for i in range(num_docs)]

    except Exception as hre:
        logger.error(f"Error during document retrieval: {hre}")
        raise HybridRetreiverError(f"Error during document retrieval: {hre}")
    logger.info(f"Retrieved {len(retrieved_docs)} documents for the query.")
    logger.debug(f"Retrieved documents: {retrieved_docs}")
    return retrieved_docs