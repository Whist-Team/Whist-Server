# syntax=docker/dockerfile:1
FROM python:3.10 as build
WORKDIR /app
ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
COPY . .
RUN poetry build

FROM python:3.10-slim
WORKDIR /app
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1
COPY --from=build /app/dist/*.whl ./
RUN pip install *.whl
CMD ["python", "-m", "whist_server", "0.0.0.0", "8080"]
