from app.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, func

class ChatHistoryModel(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, index=True, nullable=False)

    role = Column(String, nullable=False)   # "user" or "assistant"
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

