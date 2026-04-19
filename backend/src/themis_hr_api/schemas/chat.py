from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class MessageSchema(BaseModel):
    role: str
    content: str
    sentiment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChatHistoryResponse(BaseModel):
    conversation_id: int
    status: str
    messages: List[MessageSchema]

    class Config:
        from_attributes = True
