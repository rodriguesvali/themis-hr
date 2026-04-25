# Themis HR - Backend

Este diretório contém a API FastAPI e a orquestração multiagente utilizando CrewAI.
O versionamento do banco de dados relacional é gerenciado pelo Alembic.

## Execução local

Instale o backend em modo editável no ambiente virtual:

```bash
cd backend
.venv/bin/python -m pip install -e .
```

Depois execute a API:

```bash
cd backend
.venv/bin/uvicorn themis_hr_api.main:app --reload
```

Alternativa sem instalação editável:

```bash
cd backend
PYTHONPATH=src .venv/bin/uvicorn themis_hr_api.main:app --reload
```
