#!/bin/sh

## Let the DB start
python ./app/backend_pre_start.py

# Run migrations
PYTHONPATH=. alembic upgrade head

export APP_MODULE=${APP_MODULE-app.main:app}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8080}

exec uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"