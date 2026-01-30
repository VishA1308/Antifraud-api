FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y python3-setuptools

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --allow-insecure-host pypi.tuna.tsinghua.edu.cn

COPY src/ ./src/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "antifraud_service.main:app", "--host", "0.0.0.0", "--port", "8000"]