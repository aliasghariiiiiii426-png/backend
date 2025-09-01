#!/bin/sh
set -e

echo "POSTGRES_USER=$POSTGRES_USER"
echo "POSTGRES_DB=$POSTGRES_DB"
echo "POSTGRES_HOST=$POSTGRES_HOST"


# Wait for Postgres to be ready
echo "Waiting for Postgres at $POSTGRES_HOST..."
until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER"; do
  sleep 2
done

echo "Postgres is up! Starting backend..."
exec "$@"
