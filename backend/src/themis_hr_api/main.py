from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging
from themis_hr_api.core.config import settings
from themis_hr_api.schemas.chat import ChatHistoryResponse
from fastapi import HTTPException
import asyncio

from themis_hr_api.db.database import get_db, engine, Base
from themis_hr_api.models import chat
from fastapi.middleware.cors import CORSMiddleware
from themis_hr_api.orchestration.crew import ThemisHRCrew


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
        # Prepara a entrada Inicial do Router
        # Em um cenário ideal de "Agentic Routing" o Router Agent retornaria qual documento ele precisou.
        # Aqui, como o KICKOFF é fixo para a pipeline e sequencial, a LLM decidirá em run-time cruzando os Mocks em memoria:
        
        from themis_hr_api.knowledge.ferias import KNOWLEDGE_BASE_MOCK as kb_ferias
        from themis_hr_api.knowledge.admissao_contratos import KNOWLEDGE_BASE_MOCK as kb_admissao
        from themis_hr_api.knowledge.jornada_feriados import KNOWLEDGE_BASE_MOCK as kb_jornada
        from themis_hr_api.knowledge.remuneracao import KNOWLEDGE_BASE_MOCK as kb_remuneracao
        from themis_hr_api.knowledge.rescisao import KNOWLEDGE_BASE_MOCK as kb_rescisao

        mega_database = f"""
        [Base 1: Férias e Licenças]
        {kb_ferias}

        [Base 2: Admissão e Estágio]
        {kb_admissao}

        [Base 3: Jornada e DSR]
        {kb_jornada}

        [Base 4: Remuneração e Benefícios]
        {kb_remuneracao}

        [Base 5: Rescisão]
        {kb_rescisao}
        """

        inputs = {
            'user_message': request.message,
            'knowledge_base': mega_database
        }
        
        # Executa a Crew (CUIDADO: É um processo demorado chamando LLMs sequenciais)
        # O ideal no futuro do MVP é usar background_tasks ou workers (Celery/Redis)
        result = await asyncio.to_thread(ThemisHRCrew().crew().kickoff, inputs=inputs)
        
        # Fazendo parse do resultado "ESCALATE: TRUE \n MOTIVO/RESPOSTA: XYZ"
        raw_output = str(result)
        escalate = False
        bot_reply = raw_output
        
        if "ESCALATE: TRUE" in raw_output.upper():
            escalate = True
            bot_reply = raw_output.replace("ESCALATE: TRUE", "").replace("MOTIVO:", "").strip()
        else:
            bot_reply = raw_output.replace("ESCALATE: FALSE", "").replace("RESPOSTA:", "").strip()

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
