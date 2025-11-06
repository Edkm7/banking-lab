## Edkm7 ##

🎯 Objectif du projet

**Banking Lab v2** est une plateforme bancaire de démonstration basée sur une **architecture microservices**.  
Elle illustre comment construire une application sécurisée, distribuée et orchestrée avec **Docker Compose** et **HashiCorp Vault** pour la gestion des secrets.

---

## 🧩 Fonctionnalités principales

| Composant | Description | Stack |
|------------|-------------|--------|
| **Auth-Service** | Authentification, génération de JWT | FastAPI, PostgreSQL |
| **Accounts-Service** | Gestion des comptes bancaires | FastAPI, PostgreSQL |
| **Reports-Service** | Rapports et agrégations | FastAPI, PostgreSQL |
| **Web-Dashboard** | Interface d’administration | React, TailwindCSS, Nginx |
| **Vault** | Gestion des secrets (JWT, tokens) | HashiCorp Vault |
| **Database** | Stockage persistant | PostgreSQL |
| **Broker** | Communication inter-services | RabbitMQ |

---

## 🏗️ Architecture globale

```text
                  ┌───────────────────────────────┐
                  │          Web Dashboard         │
                  │ React + Tailwind + Nginx (3000)│
                  └───────────────┬───────────────┘
                                  │
          ┌───────────────────────┼─────────────────────────┐
          │                       │                         │
 ┌────────▼───────┐      ┌────────▼────────┐        ┌────────▼────────┐
 │ Auth Service   │      │ Accounts Service│        │ Reports Service │
 │ :8080          │      │ :8081           │        │ :8082           │
 └──────┬─────────┘      └────────┬────────┘        └────────┬────────┘
        │                         │                         │
        │                         │                         │
        │                         │                         │
        ▼                         ▼                         ▼
 ┌──────────────────────────────────────────────────────────────────┐
 │                    PostgreSQL Database (5432)                    │
 └──────────────────────────────────────────────────────────────────┘

                       │
                       ▼
            ┌─────────────────────┐
            │  HashiCorp Vault    │
            │  JWT + Secrets Mgmt │
            └─────────────────────┘
🗝️ Sécurité & Gestion des Secrets
🔐 Vault gère :
Le secret JWT partagé entre microservices (secret/jwt)

Le token d’accès (secrets/vault-token.txt)

Les clés d’unseal (secrets/unseal-key.txt)

⚙️ Exemple de récupération du secret :
import hvac, os

client = hvac.Client(
    url=os.getenv("VAULT_ADDR"),
    token=open("/secrets/vault-token.txt").read().strip()
)
jwt_secret_data = client.secrets.kv.v2.read_secret_version(path="secret/jwt")
JWT_SECRET = jwt_secret_data["data"]["data"]["JWT_SECRET"]
✅ Chaque microservice lit ses secrets dynamiquement au démarrage.

⚙️ Stack Technique
Couche	Technologie
Backend	FastAPI + SQLAlchemy
Frontend	React + TailwindCSS + Vite
Auth	JWT (Vault-signed secret)
Secrets	HashiCorp Vault
Database	PostgreSQL
Messaging	RabbitMQ
Containerisation	Docker Compose
Reverse Proxy	Nginx

🧠 Structure du projet

banking-lab-v2/
├── accounts-service/      # Microservice comptes
├── auth-service/          # Microservice authentification
├── reports-service/       # Microservice rapports
├── web-dashboard/         # Frontend React + Nginx
├── vault/                 # Config & data Vault
├── secrets/               # Fichiers tokens & clés (à ignorer)
├── docker-compose.yml     # Orchestration principale
└── wait-for-vault.sh      # Script d’attente de Vault
🧰 Démarrage du projet
🔧 1. Lancer l’infrastructure complète

docker compose up -d --build
Vérifie que tous les conteneurs sont démarrés :

docker ps

🔑 2. Tester les APIs
🔹 Authentification :

TOKEN_JSON=$(curl -s -X POST http://localhost:8080/auth/login \
  -d "username=alice&password=secret123")
ACCESS=$(echo $TOKEN_JSON | jq -r .access_token)
🔹 Comptes :
bash
Copier le code
curl -H "Authorization: Bearer ${ACCESS}" http://localhost:8081/accounts | jq .
🔹 Rapports :

curl -H "Authorization: Bearer ${ACCESS}" http://localhost:8082/reports/accounts-summary | jq .
💻 3. Interface Web
Accéder à :
👉 http://localhost:3000
Connectez-vous avec :

Nom d’utilisateur : alice

Mot de passe : secret123

🧩 Web Dashboard
Le dashboard admin (React + Tailwind + Nginx) offre :

🧍 Gestion des utilisateurs

💰 Visualisation des comptes

📊 Rapports de synthèse

🔐 Authentification JWT via Vault

🎨 UI moderne, responsive et fluide

🧱 Docker Compose – Services
Service	Description	Port
vault	Gestion sécurisée des secrets	8200
vault-init	Initialisation automatique de Vault	—
vault-ready	Attente du désealing de Vault	—
db	Base PostgreSQL	5432
rabbitmq	Message broker	5672 / 15672
auth-service	Auth FastAPI	8080
accounts-service	Comptes FastAPI	8081
reports-service	Rapports FastAPI	8082
web-dashboard	Front React/Nginx	3000




🚀 Améliorations futures (Infra / DevOps)
🔒 Sécurité
	• Activation du TLS sur Vault & Nginx
	• Rotation automatique des secrets JWT
	• Intégration de Vault Agent Injector
☁️ Scalabilité
	• Déploiement sur Kubernetes via Helm
	• Auto-scaling des microservices (HPA)
	• CI/CD avec GitHub Actions (build, test, scan, push images)
📊 Monitoring & Logs
	• Intégration Prometheus + Grafana
	• Centralisation des logs via ELK Stack
🧱 Base de données
	• Migration schéma via Alembic
	• Réplicas PostgreSQL pour haute disponibilité
🔄 Observabilité
	• Healthchecks sur tous les endpoints
	• Tracing distribué (Jaeger / OpenTelemetry)
	• RabbitMQ durable + Dead Letter Queues

© 2025 - Banking Lab — Designed with ❤️ by Eric DACIER

🧭 Contact
💬 Pour toute question, suggestion ou contribution :
🌐 github.com/edkm7/banking-lab-v2
📧ericdacier29@gmail.com
