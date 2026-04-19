from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging
from themis_hr_api.core.config import settings
from themis_hr_api.schemas.chat import ChatHistoryResponse
from fastapi import HTTPException

from themis_hr_api.db.database import get_db, engine, Base
from themis_hr_api.models import chat
from fastapi.middleware.cors import CORSMiddleware

# Logger setup
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# ATENÇÃO: Em produção usaremos Alembic para criar as tabelas.
# Para este mock inicial de healthcheck, não chamaremos Base.metadata.create_all aqui.
# Isso será dever do Alembic mais tarde.

app = FastAPI(title="Themis HR API", description="Multi-agent HR Helpdesk")

# Permite acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str = "anonymous"
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    reply: str
    status: str

@app.get("/health")
def health_check():
    return {"status": "ok", "app_env": settings.app_env}

@app.post("/api/v1/conversations", response_model=ChatResponse)
def init_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """ Endpoint inicial temporário - vai ser integrado com CrewAI depois """
    # 1. Cria a conversa
    new_conv = chat.Conversation(user_id=request.user_id)
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)

    # 2. Salva a mensagem do user
    user_msg = chat.Message(conversation_id=new_conv.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # MOCK de resposta do CrewAI (substituído no futuro)
    bot_reply = "Olá! Eu sou a Themis, sua assistente de RH. Recebi sua dúvida e (em breve) nossos agentes CrewAI vão processá-la."
    themis_msg = chat.Message(conversation_id=new_conv.id, role="themis", content=bot_reply)
    db.add(themis_msg)
    db.commit()

    return ChatResponse(conversation_id=new_conv.id, reply=bot_reply, status=new_conv.status)

@app.get("/api/v1/conversations/{conversation_id}", response_model=ChatHistoryResponse)
def get_chat_history(conversation_id: int, db: Session = Depends(get_db)):
    """ Retorna o histórico de uma conversa """
    conversation = db.query(chat.Conversation).filter(chat.Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    return ChatHistoryResponse(
        conversation_id=conversation.id,
        status=conversation.status,
        messages=conversation.messages
    )
