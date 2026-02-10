from app.services.retriever.build_retriever import retrieve_docs
from app.config.config import RAGConfig
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from app.services.prompting.prompt_loader import load_system_prompt
import openai
from openai import OpenAI
from langchain.agents import create_agent
from pinecone.grpc import PineconeGRPC as Pinecone
from pathlib import Path
from langgraph.checkpoint.memory import InMemorySaver 
from sqlalchemy.orm import Session
from app.models.chathistory_model import ChatHistoryModel
from app.utils.exceptions import BuildContextPromptError, RagChainError,DatabaseError, AppBaseException

from app.utils.loggers import get_logger

logger= get_logger(__name__)

# Initialize in-memory
checkpointer=InMemorySaver()

# Build dynamic prompt with retrieved context
def build_prompt_with_context(sys_config: RAGConfig):
    '''Builds a dynamic prompt function that incorporates retrieved documents into the system prompt.'''
    try:
        sys_prompt = load_system_prompt("app/resources/prompts/system_prompt.txt")

        @dynamic_prompt
        def prompt_with_context(request: ModelRequest) -> str:
            last_query = request.state["messages"][-1].text

            retrieved_docs = retrieve_docs(
                pinecone_vector_client=sys_config.pinecone_vector_client,
                index_name=sys_config.index_name,
                name_space=sys_config.name_space,
                openai_client=sys_config.openai_client,
                dense_model=sys_config.dense_model,
                dim=sys_config.dim,
                query=last_query,
                top_ret_doc=sys_config.top_ret_doc,
                alpha=sys_config.alpha,
            )

            docs_content = "\n\n".join(retrieved_docs)

            system_message = f"{sys_prompt}\n\n{docs_content}"

            return system_message
    except Exception as bcpe:
        logger.error(f"Error building context prompt: {bcpe}")
        raise BuildContextPromptError(f"Error building context prompt: {bcpe}")
    return prompt_with_context



def rag_assistant(query, build_prompt_with_contex, model,session_id):
    '''Runs the RAG assistant by creating an agent with the provided model and prompt middleware.'''
    try:
        final_answer = []
        agent = create_agent(model=model, 
                             tools=[], 
                             middleware=build_prompt_with_contex,
                             checkpointer=checkpointer)
        for step in agent.stream(
            {"messages": [{"role": "user", "content": query}]},
            {"configurable": {"thread_id": session_id}}, 
            stream_mode="values",
        ):
            
            msg = step["messages"][-1]

            if hasattr(msg, "content"):
                text = msg.content
            elif isinstance(msg, dict):
                text = msg.get("content")
            else:
                text = str(msg)

            if text:
                final_answer.append(text)
        
       
            
        answer = "".join(final_answer[-1]).strip()
    except AppBaseException as dce:
        logger.error(f"Domain error while running RAG assistant: {dce}")
        raise RagChainError

    except Exception as e:
        logger.error("Unexpected error while running RAG assistant")
        raise Exception("Unexpected error while running RAG assistant") from e

    logger.info("RAG assistant generated an answer successfully.")
    return answer or "I'm sorry, I couldn't find an answer to your question."


#store chat in db
def save_chat(sessionid: id, msg: str, role: str, db: Session):
    try: 
        db_chat= ChatHistoryModel(session_id= sessionid, role= role, content= msg)
        db.add(db_chat)
        db.commit()
        db.refresh(db_chat)

    except AppBaseException as dbe:
        logger.error(f"Error while saving chat history in database: {dbe}")
        raise DatabaseError

    except Exception as e:
        logger.error("Unexpected error while saving chat history in database.")
        raise Exception("Unexpected error while saving chat history in database.") from e