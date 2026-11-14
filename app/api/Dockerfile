
# ==========================================
# BASE
# ==========================================

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

# Install uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# ==========================================
# DEPENDENCIES - PRODUCTION
# ==========================================

FROM base AS production-deps

COPY pyproject.toml uv.lock ./

RUN uv sync \
    --frozen \
    --no-install-project \
    --no-dev

# ==========================================
# DEPENDENCIES - DEVELOPMENT
# ==========================================

FROM base AS development-deps

COPY pyproject.toml uv.lock ./

RUN uv sync \
    --frozen \
    --no-install-project

# ==========================================
# DEVELOPMENT
# ==========================================

FROM base AS development

COPY --from=development-deps /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 8000

CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]

# ==========================================
# PRODUCTION
# ==========================================

FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY --from=production-deps /opt/venv /opt/venv

COPY . .

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
