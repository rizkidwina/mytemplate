
.PHONY: up down build logs restart ps shell db-shell migrate migration test lint format

# Docker
up:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build --no-cache

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

# API
shell:
	docker compose exec api sh

# Database
db-shell:
	docker compose exec db psql -U app -d app_db

# Alembic
migration:
	docker compose run --rm api alembic revision --autogenerate -m "$(m)"

migrate:
	docker compose run --rm api alembic upgrade head

# Testing
test:
	docker compose run --rm api pytest

# Code quality
lint:
	docker compose run --rm api ruff check .

format:
	docker compose run --rm api ruff format .
