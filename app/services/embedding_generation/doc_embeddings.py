from app.utils.loggers import get_logger
from app.utils.exceptions import DocDenseEmbedError, DocSparseEmbedError
logger = get_logger(__name__)


#generate dense embeddings
def generate_dense_embeddings(text_input, dense_model,dim, openai_client): 
    try:
        res = openai_client.embeddings.create(input=text_input, model=dense_model, dimensions=dim)
        dense_embeddings = [record.embedding for record in res.data]
        
    except Exception as dde:
        logger.error(f"Error generating dense embeddings: {dde}")
        raise DocDenseEmbedError(f"Error generating dense embeddings: {dde}")
    return dense_embeddings



# Convert the chunk_text into sparse vectors
def generate_sparse_embeddings(pinecone_vector_client, text_input):
    try:
        sparse_embeddings = pinecone_vector_client.inference.embed(
        model="pinecone-sparse-english-v0",
        inputs=text_input,
        parameters={"input_type": "passage", "truncate": "END"})
    except Exception as dse:
        logger.error(f"Error generating sparse embeddings: {dse}")
        raise DocSparseEmbedError(f"Error generating sparse embeddings: {dse}")
    return sparse_embeddings