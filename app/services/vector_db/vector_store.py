
from tqdm import tqdm
import time
from app.services.embedding_generation.doc_embeddings import generate_dense_embeddings, generate_sparse_embeddings

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from app.utils.loggers import get_logger
import openai
from openai import OpenAI
from app.utils.exceptions import BatchUploadError, DatabaseConnectionError, RecordUploadError

logger = get_logger(__name__)


class VectorStoreService:
    def __init__(self, pinecone_vector_client: Pinecone, 
                openai_client: OpenAI,
                index_name: str, dim: int,
                name_space: str, dense_model: str,
                batch_size: int, sleep_time: int):
        
        #define class variables
        self.pc = pinecone_vector_client
        self.openai_client = openai_client
        self.index_name = index_name
        self.dim = dim
        self.name_space = name_space
        self.dense_model = dense_model
        self.batch_size = batch_size
        self.sleep_time = sleep_time


    def create_vector_index(self):   
        '''Create Pinecone vector index if not exists,
        with dense vector type and dotproduct metric for hybrid search'''
        try:
            if not self.pc.has_index(self.index_name):
                self.pc.create_index(
                    name=self.index_name,
                    vector_type="dense",
                    dimension=self.dim,
                    metric="dotproduct",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
        except Exception as dce:
            logger.error(f"Error creating vector index: {dce}")
            raise RecordUploadError(f"Error creating vector index: {dce}")


    def upsert_vectors(self, all_chunks):
        '''Upsert vectors into Pinecone index in batches'''
        
        try:

            for i in tqdm(range(0, len(all_chunks), self.batch_size)):
                # set end position of batch
                i_end = min(i + self.batch_size, len(all_chunks))
                # get batch of lines and IDs
                lines_batch_chunk = all_chunks[i: i_end]
                lines_batch = [d.page_content for d in lines_batch_chunk]
                ids_batch = [str(n) for n in range(i, i_end)]
                
                # create dense embeddings
                dense_embeddings = generate_dense_embeddings(text_input=lines_batch, dense_model=self.dense_model,dim=self.dim,
                                                            openai_client=self.openai_client)
                # Convert the chunk_text into sparse vectors
                sparse_embeddings = generate_sparse_embeddings(pinecone_vector_client=self.pc,
                                                            text_input=lines_batch)
                
                # prep metadata and upsert batch
                meta = [line.metadata for line in lines_batch_chunk]
                
                # upsert to Pinecone
                # Each record contains an ID, a dense vector, a sparse vector, and the original text as metadata
                records_embed = []
                for d, de, se, m, t in zip(ids_batch, dense_embeddings, sparse_embeddings, meta,lines_batch):
                    records_embed.append({
                        "id": str(d),
                        "values": de,
                        "sparse_values": {
                            "indices": se["sparse_indices"],
                            "values": se["sparse_values"]
                        },
                        "metadata": {
                            **m,
                            "text": t
                        }
                    })
                    

                # Upsert the records
                # The `chunk_text` fields are converted to dense and sparse vectors
                try:
                    index = self.pc.Index(self.index_name)
                    index.upsert(vectors= records_embed, namespace= self.name_space)
                except  Exception as bue:
                    logger.error(f"Error upserting vectors of batch {i_end}: {bue}")
                    raise BatchUploadError(f"Error upserting vectors of batch {i_end}: {bue}")
                logger.info(f"Uploaded vectors of batch {i_end}")
                time.sleep(self.sleep_time)  # Respect rate limits

        except Exception as dce:
            logger.error(f"Error upserting vectors: {dce}")
            raise RecordUploadError(f"Error upserting vectors: {dce}")