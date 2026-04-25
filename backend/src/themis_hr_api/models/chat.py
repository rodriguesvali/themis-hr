from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from themis_hr_api.db.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True) # Pode ser o id de matricula, ou nulo se anônimo
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active") # active, escalated, resolved
    
    messages = relationship("Message", back_populates="conversation", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String) # user, themis, human_agent
    content = Column(Text)
    sentiment = Column(String, nullable=True)
    category = Column(String, nullable=True)
    specialist = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    escalation_reason = Column(Text, nullable=True)
    legal_reviewed = Column(Boolean, default=False)
    legal_risk_level = Column(String, nullable=True)
    legal_notes = Column(Text, nullable=True)
    legal_basis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
