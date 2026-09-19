FROM python:3.14.0

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app

RUN uv sync --locked --no-install-project

CMD ["uv", "run", "uvicorn", "src.chat_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
