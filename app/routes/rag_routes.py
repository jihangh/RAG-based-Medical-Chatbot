from app.utils.loggers import get_logger
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.rag_schema import ChatRequest, ChatResponse, ChatHistorySchema
from app.models.chathistory_model import ChatHistoryModel
from app.services.vector_db.ensure_vector import create_vectors
from app.services.rag_chain import rag_assistant, build_prompt_with_context, save_chat
from app.utils.exceptions import AppBaseException
from app.config.config import RAGConfig
from sqlalchemy.orm import Session
from app.dependencies import get_db
import sys
import uuid

#thread_id for shorterm memory
session_id = str(uuid.uuid4()) 


config_filepath = "app/config/config.yaml"
sys_config = RAGConfig.from_yaml(config_filepath)

logger = get_logger(__name__)




router = APIRouter(prefix="/rag", tags=["rag"])

#a seperate api for embedding vectors

@router.post("/vectorstore")
async def ingest_docs():
    try:
        #chunk and embed docs into vectordb
        create_vectors(sys_config)
        return {"status": "Embeddings created and upserted to vector store"}
    except AppBaseException as abe:
        logger.exception("Vector ingestion error")
        raise HTTPException(status_code=500, detail=str(abe))
    except Exception:
        logger.exception("Unexpected vector ingestion error")
        raise HTTPException(status_code=500, detail="Internal error")



@router.post("/chat", response_model= ChatResponse)
async def chat(req: ChatRequest, db: Session=  Depends(get_db)):
    try:
        #Embed vectors in vectordb(if not already embedded)
        create_vectors(sys_config)  
        #add user message
        save_chat(sessionid= session_id, msg= req.message, role= "User", db=db)
       #chat with rag agent
        answer = rag_assistant(
            req.message,
            [build_prompt_with_context(sys_config)],
            model=sys_config.get_llm(),
            session_id=session_id
        )
        #add AI answer
        save_chat(sessionid= session_id, msg= answer, role= "AI Assistant", db=db)
        return {"answer": answer, "memory_thread_id": session_id}

    except AppBaseException as abe:
        logger.exception("Domain error in chat")
        raise HTTPException(status_code=400, detail=str(abe))

    except Exception:
        logger.exception("Unexpected error in chat")
        raise HTTPException(status_code=500, detail="Internal error")

@router.get('/chathistory', response_model= list[ChatHistorySchema])
async def get_chathistory(db: Session= Depends(get_db)):
    all_chats= db.query(ChatHistoryModel).all()
    return all_chats
