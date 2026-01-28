FROM python:3.12-slim

WORKDIR /app

# Копируем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Устанавливаем китайское зеркало
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/

COPY pyproject.toml uv.lock ./

# Убираем --locked флаг
RUN uv sync --no-dev

COPY main.py ./

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]