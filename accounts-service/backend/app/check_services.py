# check_services.py
import os
import hvac
import psycopg2
import pika

def check_vault():
    print("=== Vérification Vault ===")
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token_file = os.getenv("VAULT_TOKEN_FILE", "/secrets/vault-token.txt")

    try:
        with open(vault_token_file, "r") as f:
            vault_token = f.read().strip()
    except FileNotFoundError:
        print(f"❌ Fichier token Vault introuvable : {vault_token_file}")
        return False

    client = hvac.Client(url=vault_addr, token=vault_token)
    if not client.is_authenticated():
        print("❌ Impossible de s'authentifier auprès de Vault")
        return False

    try:
        secret = client.secrets.kv.v2.read_secret_version(path="jwt")
        jwt_secret = secret["data"]["data"]["JWT_SECRET"]
        print("✅ Vault OK, JWT_SECRET trouvé :", jwt_secret)
        return True
    except Exception as e:
        print("❌ Impossible de lire le secret JWT :", e)
        return False

def check_postgres():
    print("\n=== Vérification PostgreSQL ===")
    database_url = os.getenv("DATABASE_URL")
    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        cur.execute("\\dt")  # liste des tables
        tables = cur.fetchall()
        print("✅ PostgreSQL OK, tables existantes :")
        for t in tables:
            print(" -", t)
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("❌ Erreur PostgreSQL :", e)
        return False

def check_rabbitmq():
    print("\n=== Vérification RabbitMQ ===")
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    try:
        params = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        exchanges = channel.exchange_declare(exchange='events', exchange_type='topic', passive=True)
        print("✅ RabbitMQ OK, échange 'events' accessible")
        connection.close()
        return True
    except Exception as e:
        print("❌ Erreur RabbitMQ :", e)
        return False

if __name__ == "__main__":
    v_ok = check_vault()
    db_ok = check_postgres()
    rmq_ok = check_rabbitmq()
    if v_ok and db_ok and rmq_ok:
        print("\n🎉 Tout est opérationnel !")
    else:
        print("\n⚠️ Il y a des erreurs à corriger.")
