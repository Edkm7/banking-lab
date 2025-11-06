import os
import hvac

# ==========================
# Variables d'environnement
# ==========================
VAULT_ADDR = os.getenv("VAULT_ADDR", "http://vault:8200")
VAULT_TOKEN_FILE = os.getenv("VAULT_TOKEN_FILE", "/secrets/vault-token.txt")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/banking")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

# ==========================
# Lecture du token Vault
# ==========================
try:
    with open(VAULT_TOKEN_FILE, "r") as f:
        VAULT_TOKEN = f.read().strip()
except FileNotFoundError:
    raise RuntimeError(f"Le fichier de token Vault '{VAULT_TOKEN_FILE}' est introuvable")

# ==========================
# Connexion à Vault
# ==========================
client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
if not client.is_authenticated():
    raise RuntimeError("Impossible de s'authentifier auprès de Vault avec le token fourni")

# ==========================
# Lecture du secret JWT
# ==========================
try:
    jwt_secret_data = client.secrets.kv.v2.read_secret_version(path="jwt")
    JWT_SECRET = jwt_secret_data["data"]["data"]["JWT_SECRET"]
except hvac.exceptions.Forbidden:
    raise RuntimeError("Permission denied: vérifie que le token Vault a accès à 'secret/data/jwt'")
except hvac.exceptions.InvalidPath:
    raise RuntimeError("Le secret 'jwt' n'existe pas dans Vault à l'emplacement 'secret/'")

# ==========================
# Autres constantes
# ==========================
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# ==========================
# Objet Settings
# ==========================
class Settings:
    JWT_SECRET = JWT_SECRET
    ALGORITHM = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
    DATABASE_URL = DATABASE_URL
    VAULT_ADDR = VAULT_ADDR
    RABBITMQ_URL = RABBITMQ_URL

settings = Settings()
