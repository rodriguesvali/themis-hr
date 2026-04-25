#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r .devcontainer/requirements-bootstrap.txt
npm install -g @angular/cli

(
  cd backend
  python -m pip install -r requirements.txt
  python -m pip install -e .
  alembic upgrade head
)
