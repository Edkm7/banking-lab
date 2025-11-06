#!/bin/sh
set -e

# --- Wait for Postgres ---
echo "⏳ Waiting for database to be ready at $DATABASE_URL..."
until pg_isready -h db -p 5432 -U postgres > /dev/null 2>&1; do
  echo "Database not ready yet, retrying..."
  sleep 7
done
echo "✅ Database is ready."

# --- Wait for Vault ---
echo "⏳ Waiting for Vault to be ready at $VAULT_ADDR..."
until curl -s $VAULT_ADDR/v1/sys/health | grep -q '"sealed":false'; do
  echo "Vault is sealed or unavailable, waiting..."
  sleep 7
done
echo "✅ Vault is ready and unsealed."

# --- Start app ---
exec "$@"
