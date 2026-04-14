FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    git \
    curl \
    make \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/mega_projekt

COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e "/workspaces/django_blog[dev]"


COPY . .


EXPOSE 8000