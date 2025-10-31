# 🏦 Banking Lab — Architecture Microservices avec Docker Compose

## 📘 Présentation

Ce projet illustre une **architecture bancaire microservices** hébergée avec **Docker Compose**.  
Chaque service est isolé dans son propre conteneur et communique avec les autres via le réseau Docker.

### ⚙️ Composition du système

| Service | Technologie | Rôle |
|----------|--------------|------|
| 🐘 **postgres** | PostgreSQL 15 | Base de données partagée |
| 🔐 **auth-service** | Spring Boot (Java 17) + JWT | Authentification et gestion des utilisateurs |
| 💳 **accounts-service** | FastAPI (Python) | Gestion des comptes bancaires |
| 📊 **reports-service** | Node.js | Génération et agrégation de rapports |
| 💻 **web-dashboard** | React | Interface utilisateur web |

---

## 🧩 Architecture globale

[ Web Dashboard (React) ]
|
v
[ Auth Service (Spring Boot) ] <--> [ PostgreSQL ]
|
v
[ Accounts Service (FastAPI) ] <--> [ PostgreSQL ]
|
v
[ Reports Service (Node.js) ] (utilise les APIs des autres services)

yaml
Copier le code

---

## 🐳 Démarrage avec Docker Compose

### 🔧 Prérequis
- Docker et Docker Compose installés
- Port non utilisé : `3000`, `8081`, `8082`, `8083`, `5432`

### 🚀 Lancer le projet

```bash
docker-compose up --build
Les conteneurs seront construits, puis exécutés automatiquement.

🌍 Points d’accès
Service	URL locale	Description
PostgreSQL	localhost:5432	Base de données
Auth Service	http://localhost:8082	API Spring Boot
Accounts Service	http://localhost:8081	API FastAPI
Reports Service	http://localhost:8083	API Node.js
Web Dashboard	http://localhost:3000	Interface web

🧠 Flux typique d’utilisation
L’utilisateur s’inscrit ou se connecte via le web-dashboard, qui envoie les requêtes à auth-service.

auth-service vérifie les identifiants, puis génère un JWT.

Ce token JWT est stocké côté client (dans le navigateur).

Les appels suivants (vers accounts-service et reports-service) incluent le token :

makefile
Copier le code
Authorization: Bearer <JWT>
Chaque service vérifie la validité du token avant d’exécuter la requête.

🧰 Variables d’environnement
Service	Variable	Description
postgres	POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB	Identifiants DB
auth-service	SPRING_DATASOURCE_URL, SPRING_DATASOURCE_USERNAME, SPRING_DATASOURCE_PASSWORD	Connexion DB
accounts-service	POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD	Connexion DB
reports-service	ACCOUNTS_URL	URL du service de comptes

🧪 Vérification
Une fois les conteneurs démarrés :

bash
Copier le code
curl http://localhost:8082/actuator/health
✅ Réponse attendue :

json
Copier le code
{"status": "UP"}
🧹 Arrêter et nettoyer
bash
Copier le code
docker-compose down
Pour tout supprimer (y compris les volumes de la base) :

bash
Copier le code
docker-compose down -v
📁 Structure du projet
Copier le code
banking-lab/
├── auth-service/
├── accounts-service/
├── reports-service/
├── web-dashboard/
├── docker-compose.yml
└── README.md
👨‍💻 Auteur
Edkm7
Projet d’apprentissage Docker + Microservices
📚 Objectif : Comprendre les communications interservices et la conteneurisation d’une architecture complète.
