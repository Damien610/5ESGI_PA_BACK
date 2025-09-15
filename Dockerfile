FROM python:3.11-slim

WORKDIR /app

# Outils utiles
RUN apt-get update \
 && apt-get install -y --no-install-recommends netcat-openbsd dos2unix \
 && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code applicatif
COPY . .

# Copier l'entrypoint dans un endroit NON écrasé par le volume
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN dos2unix /usr/local/bin/entrypoint.sh \
 && chmod +x /usr/local/bin/entrypoint.sh

# Optionnel: garde aussi un point d'entrée par défaut dans l'image
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
