#!/bin/sh

echo "⏳ Waiting for PostgreSQL to start..."
until pg_isready -h db -p 5432; do
    echo "Waiting for database..."
    sleep 1
done
echo "✅ PostgreSQL is up and running!"

echo "🚀 Running Alembic migrations (PROD)..."
alembic upgrade head  # ✅ 운영 환경에서 DB 마이그레이션 자동 실행

echo "🔥 Starting FastAPI..."
if [ "$ENV" = "dev" ]; then
    exec python -m uvicorn src.dispatch.main:app --host 0.0.0.0 --port=8000 --reload
else
    exec uvicorn src.dispatch.main:app --host 0.0.0.0 --port=8000
fi
