#!/usr/bin/env bash
set -euo pipefail

echo "==> Bootstrapping service"

# Valeurs par défaut sûres si non fournies
: "${POSTGRES_HOST:=db_prod}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_USER:=postgres}"
: "${POSTGRES_PASSWORD:=postgres}"
: "${POSTGRES_DB:=postgres}"
: "${RUN_MIGRATIONS:=true}"     # mets à "false" si tu veux désactiver les migrations au boot
: "${ALEMBIC_INI:=alembic.ini}" # chemin vers ton alembic.ini
: "${MIGRATION_CMD:=alembic -c ${ALEMBIC_INI} upgrade head}"

# DATABASE_URL prioritaire si déjà défini (ex: via secrets)
if [[ -z "${DATABASE_URL:-}" ]]; then
  export DATABASE_URL="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
fi

echo "Using DATABASE_URL=${DATABASE_URL//:*@/:****@}"  # masque le mot de passe dans les logs

# 1) Attendre PostgreSQL (avec timeout et retries)
echo "==> Waiting for PostgreSQL ${POSTGRES_HOST}:${POSTGRES_PORT} ..."
retries=60
until nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}" >/dev/null 2>&1; do
  ((retries--)) || { echo "❌ Postgres not reachable after 60s"; exit 1; }
  sleep 1
done
echo "✅ PostgreSQL reachable"

# 2) Exécuter les migrations (idempotent) si activé
if [[ "${RUN_MIGRATIONS}" == "true" ]]; then
  echo "==> Running migrations: ${MIGRATION_CMD}"
  # petit retry si Postgres répond mais n'est pas totalement prêt
  tries=3
  until ${MIGRATION_CMD}; do
    ((tries--)) || { echo "❌ Alembic failed after retries"; exit 1; }
    echo "Alembic failed, retrying in 3s..."
    sleep 3
  done
  echo "✅ Migrations applied"
else
  echo "⚠️ RUN_MIGRATIONS=false -> skipping migrations"
fi

# 3) Démarrer l’application
echo "==> Starting app: $*"
exec "$@"
=======
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