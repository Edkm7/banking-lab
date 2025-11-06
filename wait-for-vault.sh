#!/bin/sh
set -e

echo "⏳ Waiting for Vault to be unsealed and ready..."
until curl -s http://vault:8200/v1/sys/health | grep -q '"sealed":false'; do
  sleep 2
done
echo "✅ Vault is ready!"
