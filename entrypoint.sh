#!/usr/bin/env bash
set -euo pipefail

echo "$(date '+%Y-%m-%d %H:%M:%S') ==> Bootstrapping service"

# Valeurs par défaut
: "${POSTGRES_HOST:=db_dev}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_USER:=dev}"
: "${POSTGRES_PASSWORD:=dev}"
: "${POSTGRES_DB:=app_db_dev}"
: "${RUN_MIGRATIONS:=true}"
: "${SEED_DATA:=true}"

# 1) Attendre PostgreSQL
echo "$(date '+%Y-%m-%d %H:%M:%S') ==> Waiting for PostgreSQL ${POSTGRES_HOST}:${POSTGRES_PORT}"
retries=60
until nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}" >/dev/null 2>&1; do
  ((retries--)) || { echo "$(date '+%Y-%m-%d %H:%M:%S') ❌ Postgres not reachable after 60s"; exit 1; }
  sleep 1
done
echo "$(date '+%Y-%m-%d %H:%M:%S') ✅ PostgreSQL reachable"

# 2) Exécuter les migrations
if [[ "${RUN_MIGRATIONS}" == "true" ]]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') ==> Running migrations: alembic -c alembic.ini upgrade head"
  tries=5
  until alembic -c alembic.ini upgrade head; do
    ((tries--)) || { echo "$(date '+%Y-%m-%d %H:%M:%S') ❌ Alembic failed after retries"; exit 1; }
    echo "$(date '+%Y-%m-%d %H:%M:%S') Alembic failed, retrying in 3s..."
    sleep 3
  done
  echo "$(date '+%Y-%m-%d %H:%M:%S') ✅ Migrations applied"
fi

# 3) Insérer les données de test
if [[ "${SEED_DATA}" == "true" ]]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') ==> Seeding test data"
  python3 << 'PYEOF'
import psycopg2
import os

try:
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'db_dev'),
        port=os.getenv('POSTGRES_PORT', '5432'),
        user=os.getenv('POSTGRES_USER', 'dev'),
        password=os.getenv('POSTGRES_PASSWORD', 'dev'),
        database=os.getenv('POSTGRES_DB', 'app_db_dev')
    )
    cur = conn.cursor()
    
    # Vérifier si les données existent déjà
    cur.execute("SELECT COUNT(*) FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03'")
    if cur.fetchone()[0] == 0:
        # Restaurant
        cur.execute("""
            INSERT INTO restaurant (uri_name, name, logo, uuid)
            VALUES ('shake-shack', 'Shake Shack', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Shake_Shack_logo.svg/2560px-Shake_Shack_logo.svg.png', '2f973077-158e-4337-8507-ff348e99bf03')
        """)
        
        # Terminaux
        cur.execute("""
            INSERT INTO terminal (uuid, name, id_restaurant)
            VALUES 
              ('cebbe9f9-637b-4220-aad4-7ab299c007f1', 'Borne 001', (SELECT id_restaurant FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03')),
              ('57ec4e4c-533a-4854-98cd-c00360805eed', 'Borne 002', (SELECT id_restaurant FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03'))
        """)
        
        # Styles
        cur.execute("""
            INSERT INTO style (uuid, name, style_value, id_restaurant)
            VALUES 
              ('43b35977-bf79-4ca7-b046-017fe2871986', 'primary', 'oklch(0.553 0.158 136.559)', (SELECT id_restaurant FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03')),
              ('ae38585e-8e26-4341-9442-bea52bdafe97', 'primary-foreground', 'oklch(0.984 0.003 247.858)', (SELECT id_restaurant FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03'))
        """)
    
        conn.commit()
        print("Data seeded successfully")
    else:
        print("Data already exists")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Seed failed: {e}")
PYEOF
  echo "$(date '+%Y-%m-%d %H:%M:%S') ✅ Test data seeded"
fi

# 4) Démarrer l'application
echo "$(date '+%Y-%m-%d %H:%M:%S') ==> Starting app: $*"
exec "$@"
