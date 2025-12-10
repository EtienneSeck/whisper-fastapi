# Utiliser une image officielle Python légère
FROM python:3.11-slim

# Variables d'environnement pour éviter les prompts interactifs
ENV PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/cache \
    HF_HOME=/cache

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Créer un dossier pour le cache Hugging Face
RUN mkdir -p /cache

# Copier requirements et installer les packages Python
RUN pip install --no-cache-dir --upgrade pip

# Installer torch, transformers et fastapi + uvicorn
RUN pip install --no-cache-dir \
    torch \
    transformers[torch] \
    fastapi[all]

# Copier le code de l'application
WORKDIR /app
COPY . /app

# Exposer le port FastAPI
EXPOSE 7860

# Commande de lancement
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]