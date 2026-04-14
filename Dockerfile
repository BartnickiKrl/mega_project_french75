# 1. Obraz bazowy - najnowszy stabilny Python na lekkim Debianie
FROM python:3.12-slim

# 2. Ustawienia środowiskowe
# PYTHONDONTWRITEBYTECODE: wyłącza tworzenie plików .pyc (zbędne w kontenerze)
# PYTHONUNBUFFERED: wymusza natychmiastowe wypisywanie logów (widzisz błędy Django od razu)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Instalacja zależności systemowych
# Potrzebujemy git do VS Code i libpq-dev jeśli kiedyś przejdziesz na PostgreSQL
RUN apt-get update && apt-get install -y \
    git \
    curl \
    make \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Katalog roboczy wewnątrz kontenera
WORKDIR /workspaces/django_blog

# 5. Instalacja zależności Pythona
# Najpierw kopiujemy tylko plik z zależnościami, żeby Docker mógł użyć cache
COPY pyproject.toml .

# Instalujemy pip i nasz projekt w trybie edytowalnym z dodatkami dev
# Flaga -e (editable) pozwala na zmiany w kodzie bez przeinstalowywania paczki
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e "/workspaces/django_blog[dev]"

# 6. Kopiujemy resztę plików (choć VS Code i tak je zamontuje przez Volume)
COPY . .

# 7. Port dla Django
EXPOSE 8000