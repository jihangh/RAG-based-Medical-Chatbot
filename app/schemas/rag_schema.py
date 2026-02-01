from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    
    
class ChatResponse(BaseModel):
    answer: str
    memory_thread_id: str