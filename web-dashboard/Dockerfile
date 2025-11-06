# Étape 1 : Builder React
FROM node:20-alpine AS builder

WORKDIR /app

# Copier les fichiers package
COPY package*.json ./

# Installer les dépendances
RUN npm install --legacy-peer-deps

# Copier le reste de l'application
COPY . .

# Construire l'application pour production
RUN npm run build

# Étape 2 : Servir avec Nginx
FROM nginx:alpine

# Supprimer le contenu par défaut
RUN rm -rf /usr/share/nginx/html/*

# Copier le build React depuis l'étape précédente
COPY --from=builder /app/build /usr/share/nginx/html

# Copier le nginx.conf custom
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]
