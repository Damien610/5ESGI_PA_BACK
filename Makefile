# 🔧 Environnement de développement
# 🛠 Dev
dev-up:
	docker compose -p app_dev -f docker-compose.yml --env-file .env.dev up --build -d

dev-down:
	docker compose -p app_dev -f docker-compose.yml --env-file .env.dev down --remove-orphans

dev-logs:
	docker compose -p app_dev -f docker-compose.yml --env-file .env.dev logs -f

dev-bash-api:
	docker exec -it fastapi_projet_dev bash

dev-bash-db:
	docker exec -it postgres_dev bash
# 🚀 Prod
prod-up:
	docker compose -p app_prod -f docker-compose.prod.yml --env-file .env.prod up --build -d

prod-down:
	docker compose -p app_prod -f docker-compose.prod.yml --env-file .env.prod down --remove-orphans

prod-logs:
	docker compose -p app_prod -f docker-compose.prod.yml --env-file .env.prod logs -f

prod-bash-api:
	docker exec -it fastapi_projet_prod bash

prod-bash-db:
	docker exec -it postgres_prod bash


# ⚙️ Alembic
migrate:
	docker exec -it fastapi_projet_dev alembic revision --autogenerate -m "$(msg)"

upgrade:
	docker exec -it fastapi_projet_dev alembic upgrade head

downgrade:
	docker exec -it fastapi_projet_dev alembic downgrade -1

seed:
	docker exec -it fastapi_projet_dev psql -h db_dev -U dev -d app_db_dev -f /app/scripts/seed_data.sql

# 🧪 Tests et qualité du code
lint:
	flake8 app

format:
	black app

test:
	pytest tests