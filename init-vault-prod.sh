#!/bin/sh
set -e

VAULT_ADDR="http://vault:8200"
UNSEAL_KEY_FILE="/secrets/unseal-key.txt"
TOKEN_FILE="/secrets/vault-token.txt"

echo "⏳ Waiting for Vault API..."
until curl -s -o /dev/null -w "%{http_code}" $VAULT_ADDR/v1/sys/health | grep -E "200|429|472|473|501|503" >/dev/null; do
  echo "   ...still waiting..."
  sleep 3
done
echo "✅ Vault API reachable."


# Vérifie si Vault est déjà unsealed
if vault status | grep -q "Sealed *false"; then
  echo "✅ Vault already unsealed."
else
  
  echo "🔓 Unsealing Vault..."
  while IFS= read -r key; do
    if [ -n "$key" ]; then
      echo "→ Applying unseal key..."
      vault operator unseal "$key" >/dev/null
    fi
  done < "$UNSEAL_KEY_FILE"
fi

# Auth avec le token root
vault login $(cat "$TOKEN_FILE") >/dev/null 2>&1 || true

# (Optionnel) Vérifie le secret JWT
vault kv get secret/jwt >/dev/null 2>&1 || {
  echo "⚙️ Creating JWT secret..."
  vault kv put secret/jwt JWT_SECRET="supersecretkey12345"
}

echo "✅ Vault unsealed and ready!"
