from app.services.vector_db.vector_store import VectorStoreService
from app.services.data_ingestion.data_loader import load_pdf
from app.services.data_ingestion.data_processor import medical_filter_docs
from app.services.data_ingestion.data_chunker import chunk_documents
from app.utils.loggers import get_logger
from app.utils.exceptions import BuildKnowledgeBaseError
from app.config.config import RAGConfig

logger= get_logger(__name__)



def build_medical_vector_store(config: RAGConfig):
    '''Build medical vector store from PDF document'''
    try:
        #load PDF into documents
        pdf_docs = load_pdf(config.url, config.pdfname)
        #filter and preprocess documents
        processed_docs= medical_filter_docs(pdf_docs)

        #chunk document
        chunks = chunk_documents(processed_docs, config.chunk_size, config.chunk_overlap)
           
        logger.info(chunks[0:3])
        #initialize VectorStoreService
        vector_store_service = VectorStoreService(
            config.pinecone_vector_client,
            config.openai_client,
            config.index_name,
            config.dim,
            config.name_space,
            config.dense_model,
            config.batch_size,
            config.sleep_time
        )
        #create Pinecone vector index if not exists
        vector_store_service.create_vector_index()

        # #generate dense and sparse embeddings and upsert them into Pinecone
        vector_store_service.upsert_vectors(all_chunks=chunks)
    except Exception as bkbe:
        logger.error(f"Error building medical vector store: {bkbe}") 
        raise BuildKnowledgeBaseError(f"Failed to build medical vector store: {bkbe}")
     

    return


