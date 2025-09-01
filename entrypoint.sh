#!/bin/sh
set -e

# Default values (can override via .env)
POSTGRES_HOST=${POSTGRES_HOST:-shopify_postgres}
POSTGRES_USER=${POSTGRES_USER:-behnam}
POSTGRES_DB=${POSTGRES_DB:-shopify_db}

echo "Waiting for Postgres at $POSTGRES_HOST..."

# Wait until Postgres is ready
until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER"; do
  sleep 2
done

echo "Postgres is up! Starting backend..."

# Start the backend with exec to prevent shell from exiting
exec uvicorn main:app --host 0.0.0.0 --port 8000

