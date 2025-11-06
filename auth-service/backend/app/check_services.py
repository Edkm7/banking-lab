# check_services.py
import os
import hvac
import psycopg2
import pika

SERVICES = {
    "auth-service": {"db_schema": "auth", "db_url": os.getenv("AUTH_DATABASE_URL", os.getenv("DATABASE_URL"))},
    "accounts-service": {"db_schema": "accounts", "db_url": os.getenv("ACCOUNTS_DATABASE_URL", os.getenv("DATABASE_URL"))},
}

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
    ok = True
    for service, cfg in SERVICES.items():
        db_url = cfg["db_url"]
        try:
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
            """)
            tables = cur.fetchall()
            print(f"✅ {service} OK, tables existantes :")
            for t in tables:
                print(" -", t[0])
            cur.close()
            conn.close()
        except Exception as e:
            print(f"❌ Erreur PostgreSQL ({service}) :", e)
            ok = False
    return ok

def check_rabbitmq():
    print("\n=== Vérification RabbitMQ ===")
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    try:
        params = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        try:
            channel.exchange_declare(exchange='events', exchange_type='topic', passive=True)
            print("✅ RabbitMQ OK, échange 'events' accessible")
        except pika.exceptions.ChannelClosedByBroker as e:
            print(f"⚠️ Échange 'events' non trouvé : {e}")
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
        print("\n🎉 Tous les services sont opérationnels !")
    else:
        print("\n⚠️ Il y a des erreurs à corriger.")
