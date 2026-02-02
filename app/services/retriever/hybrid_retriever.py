from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from app.utils.loggers import get_logger
import openai
from openai import OpenAI
from app.utils.exceptions import HybridSearchError

logger = get_logger(__name__)

class HybridRetriever:
    """Hybrid Retriever combining dense and sparse retrieval methods."""

    def __init__(self, pinecone_vector_client: Pinecone, index_name: str, name_space: str):
        self.pc = pinecone_vector_client
        self.index_name = index_name
        self.name_space = name_space

    def hybrid_score_norm(self, dense, sparse, alpha: float):
        """Hybrid score using a convex combination

        alpha * dense + (1 - alpha) * sparse

        Args:
            dense: Array of floats representing
            sparse: a dict of `indices` and `values`
            alpha: scale between 0 and 1
        """
        if alpha < 0 or alpha > 1:
            raise ValueError("Alpha must be between 0 and 1")
        hs = {
            'indices': sparse['sparse_indices'],
            'values':  [v * (1 - alpha) for v in sparse['sparse_values']]
        }
        return [v * alpha for v in dense], hs


    def contextual_hybrid_search(self, dense_query_embedding, sparse_query_embedding, top_ret_doc: int, alpha: float):
        
        """Perform hybrid search on Pinecone index using dense and sparse query embeddings."""
        try:
            for sparse, dense in zip(sparse_query_embedding, dense_query_embedding):
                hdense, hsparse = self.hybrid_score_norm(dense, sparse, alpha=alpha)
                index = self.pc.Index(self.index_name)
                query_response = index.query(
                namespace= self.name_space,
                top_k=top_ret_doc,
                vector=hdense,
                sparse_vector=hsparse,
                include_values=False,
                include_metadata=True
            )
        except Exception as hse:
            logger.error(f"Error during hybrid search: {hse}")
            raise HybridSearchError(f"Error during hybrid search: {hse}")
        return query_response