#!/bin/bash
set -euo pipefail

# Valeurs par défaut si non fournies par .env.dev
: "${POSTGRES_HOST:=db_dev}"
: "${POSTGRES_PORT:=5432}"
echo "Using PostgreSQL host: $POSTGRES_HOST"
echo "Using PostgreSQL port: $POSTGRES_PORT"
echo "Waiting for PostgreSQL ($POSTGRES_HOST:$POSTGRES_PORT) to be ready..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "PostgreSQL is ready. Starting app..."
exec "$@"
