from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging
from themis_hr_api.core.config import settings
from themis_hr_api.schemas.chat import ChatHistoryResponse
from fastapi import HTTPException
import asyncio

from themis_hr_api.db.database import get_db
from themis_hr_api.models import chat
from fastapi.middleware.cors import CORSMiddleware
from themis_hr_api.orchestration.crew import ThemisHRCrew


# Logger setup
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# ATENÇÃO: o schema é gerenciado pelo Alembic; a API não cria tabelas automaticamente.

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
async def init_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """ Endpoint de conversa com a Engine Multiagente CrewAI rodando síncrona """
    # 1. Cria a conversa
    new_conv = chat.Conversation(user_id=request.user_id)
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)

    # 2. Salva a mensagem do user
    user_msg = chat.Message(conversation_id=new_conv.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    try:
        # Fluxo condicional: principal_agent classifica e apenas o especialista necessário é chamado.
        result = await asyncio.to_thread(ThemisHRCrew().run, request.message)
        bot_reply = result.reply
        escalate = result.should_escalate

    except Exception as e:
        logger.error(f"Erro na engine da CrewAI: {e}")
        bot_reply = "Perdão, minha central de processamento (LLM) falhou no momento ou sua chave de IA é inválida. Tente novamente mais tarde."
        escalate = False

    # Gravar status de escalonamento se ocorreu
    if escalate:
        new_conv.status = "escalated"
        db.add(new_conv)

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
