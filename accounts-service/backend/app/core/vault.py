import os
import hvac

def get_jwt_secret():
    vault_addr = os.getenv("VAULT_ADDR", "http://vault:8200")
    vault_token = os.getenv("VAULT_TOKEN", "root")

    client = hvac.Client(url=vault_addr, token=vault_token)

    # Lecture du secret stocké à secret/data/jwt
    secret = client.secrets.kv.v2.read_secret_version(path="jwt")
    return secret["data"]["data"]["JWT_SECRET"]
