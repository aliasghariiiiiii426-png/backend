#!/bin/sh
set -e

echo "Waiting for Postgres..."
until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  sleep 2
done
echo "Postgres is ready"

# Create database if it doesn't exist
DB_EXISTS=$(psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")
if [ "$DB_EXISTS" != "1" ]; then
  echo "Creating database $POSTGRES_DB..."
  psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB;"
fi

# Start FastAPI app with Uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
