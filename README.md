
# FastAPI Backend Starter Template

A production-minded backend starter template built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, and Docker.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 16
- SQLAlchemy 2
- Alembic
- Pydantic
- Pydantic Settings
- uv
- Docker & Docker Compose
- Pytest
- Ruff
- Mypy

## Project Structure

```text
app/api/
├── api/
├── core/
├── db/
├── features/
├── migrations/
├── tests/
├── Dockerfile
├── main.py
├── pyproject.toml
├── uv.lock
└── alembic.ini
```

## Requirements

- Docker Desktop
- Docker Compose

Python and project dependencies are managed inside Docker.

## Environment Setup

1. Clone this repository.
2. Copy `.env.example` to `.env`.
3. Configure the required environment variables.
4. Build and start the services.

```bash
docker compose up -d --build
```

## Development

Start development services:

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f api
```

Stop services:

```bash
docker compose down
```

## Database Migrations

Create a migration:

```bash
docker compose run --rm api alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
docker compose run --rm api alembic upgrade head
```

Check current migration:

```bash
docker compose run --rm api alembic current
```

## Testing

```bash
docker compose run --rm api pytest
```

## Code Quality

```bash
docker compose run --rm api ruff check .
docker compose run --rm api ruff format .
docker compose run --rm api mypy .
```

## Production

```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d --build
```
