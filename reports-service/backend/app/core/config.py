import os
import hvac

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://vault:8200")
VAULT_TOKEN_FILE = os.getenv("VAULT_TOKEN_FILE", "/secrets/vault-token.txt")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/banking")

# Lire le token Vault
try:
    with open(VAULT_TOKEN_FILE, "r") as f:
        VAULT_TOKEN = f.read().strip()
except FileNotFoundError:
    VAULT_TOKEN = os.getenv("VAULT_TOKEN", None)

JWT_SECRET = os.getenv("JWT_SECRET", None)

if not JWT_SECRET:
    try:
        client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
        if client.is_authenticated():
            data = client.secrets.kv.v2.read_secret_version(path="jwt")
            JWT_SECRET = data["data"]["data"]["JWT_SECRET"]
            print(f"✅ JWT_SECRET successfully loaded from Vault: {JWT_SECRET[:5]}...")
        else:
            print("❌ Vault client not authenticated.")
    except Exception as e:
        print(f"❌ Error reading JWT_SECRET from Vault: {e}")
        JWT_SECRET = None

ALGORITHM = "HS256"
