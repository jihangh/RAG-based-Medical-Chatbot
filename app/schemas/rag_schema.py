from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    
    
class ChatResponse(BaseModel):
    answer: str
    memory_thread_id: str



class ChatHistorySchema(BaseModel):
    id: int

    session_id: str

    role: str
    content: str

    created_at :datetime

    model_config = ConfigDict(from_attributes=True)