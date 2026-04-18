FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    git \
    curl \
    make \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/mega_project_french75/letterboxd_stats

COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[dev]"


COPY . .

WORKDIR /workspaces/mega_project_french75/letterboxd_stats

EXPOSE 8000

CMD ["find", ".", "-maxdepth", "3", "-name", "manage.py"]