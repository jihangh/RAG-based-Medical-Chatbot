from app.utils.exceptions import QueryDenseEmbedError, QuerySparseEmbedError
from app.utils.loggers import get_logger
logger = get_logger(__name__)


def generate_query_embeddings(query, dense_model,dim, openai_client, pinecone_vector_client):
    """Generate dense and sparse embeddings for a query."""
    try:
        # Convert the query into a dense vector
        dense_query_embed = openai_client.embeddings.create(input=query, model=dense_model, dimensions=dim)
        dense_query_embedding = [record.embedding for record in dense_query_embed.data]
    except Exception as qde:
        logger.error(f"Error generating dense query embeddings: {qde}")
        raise QueryDenseEmbedError(f"Error generating dense query embeddings: {qde}")

    try:
        # Convert the query into a sparse vector
        sparse_query_embedding = pinecone_vector_client.inference.embed(
            model="pinecone-sparse-english-v0",
            inputs=query,
            parameters={"input_type": "query", "truncate": "END"}
        )
    except Exception as qse:
        logger.error(f"Error generating sparse query embeddings: {qse}")
        raise QuerySparseEmbedError(f"Error generating sparse query embeddings: {qse}")
    
    logger.info("Generated query embeddings successfully.")
    return dense_query_embedding, sparse_query_embedding