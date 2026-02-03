import re
from langchain_core.documents import Document
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.utils.loggers import get_logger
from app.utils.exceptions import DataProcessingError
logger= get_logger(__name__)



#remove unwanted prefixes (. or :) from chunks
def clean_chunk_prefix(text: str) -> str:
    return re.sub(r'^[.:]\s*', '', text)


#chunk documents into smaller pieces
def chunk_documents(docs, chunk_size: int, chunk_overlap: int) -> List[Document]:
    """Chunk documents into smaller pieces"""

    try:    
        #recursiveCharacterTextSplitter with medical-specific separators
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,         # Ideal for clinical explanations
        chunk_overlap=chunk_overlap,      # Preserves continuity
        separators=["\n\n",             # Section boundaries 
                    "\n",               # Paragraph boundaries
                    ".",                # Sentence boundary
                    ";",
                    ",",                # Sentence boundary 
                    " "
                ]
                )
        
        all_chunks = []
        
        chunks = text_splitter.split_documents(docs)
        for chunk in chunks:
                src= chunk.metadata.get('source')
                pg= chunk.metadata.get('page')
                temp_doc= Document(metadata={"page": pg, "source": src},
                        page_content= clean_chunk_prefix(chunk.page_content))
                all_chunks.append(temp_doc)
        logger.info(f"Chunked documents into {len(all_chunks)} pieces")
    except Exception as e:
        logger.error(f"Data processing error in chunk_documents: {e}")
        raise DataProcessingError(f"Failed to chunk documents due to data processing error: {e}")
    logger.info(f"{len(all_chunks)} Text chunks obtained")
    return all_chunks