# 🔧 Environnement de développement
dev-up:
	docker-compose up --build

dev-down:
	docker-compose down --volumes --remove-orphans

dev-logs:
	docker-compose logs -f

dev-bash-api:
	docker exec -it fastapi_projet_dev bash

dev-bash-db:
	docker exec -it postgres_dev bash

# 🚀 Environnement de production
prod-up:
	docker-compose -f docker-compose.prod.yml up --build -d

prod-down:
	docker-compose -f docker-compose.prod.yml down --volumes --remove-orphans

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

prod-bash-api:
	docker exec -it fastapi_projet_prod bash

prod-bash-db:
	docker exec -it postgres_prod bash

# ⚙️ Alembic
migrate:
	alembic revision --autogenerate -m "$(msg)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

# 🧪 Tests et qualité du code
lint:
	flake8 app

format:
	black app

test:
	pytest tests