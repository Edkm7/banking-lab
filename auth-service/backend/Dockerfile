# auth-service/backend/Dockerfile

FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Variables d'environnement
ENV PYTHONUNBUFFERED=1

# Copier uniquement requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt hvac

# Copier tout le contenu de backend dans /app
COPY . .

# Vérifier que Python voit les packages
ENV PYTHONPATH=/app

# Exposer le port FastAPI
EXPOSE 8080
COPY wait-for-db.sh /wait-for-db.sh
# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
