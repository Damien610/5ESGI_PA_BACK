
up:
	docker-compose up --build

down:
	docker-compose down --volumes --remove-orphans

logs:
	docker-compose logs -f

bash-api:
	docker exec -it fastapi_projet bash

bash-db:
	docker exec -it postgres bash

# ⚙️ Alembic
migrate:
	alembic revision --autogenerate -m "$(msg)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1


lint:
	flake8 app

format:
	black app

test:
	pytest tests

