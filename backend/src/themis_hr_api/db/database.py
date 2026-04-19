from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from themis_hr_api.core.config import settings

# Conexão com o banco (Postgres do DevContainer ou SQLite fallback)
engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
