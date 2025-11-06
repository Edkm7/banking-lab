import pika, json, threading, logging
from .config import settings
from app.api.events import handle_user_created

params = pika.URLParameters(settings.RABBITMQ_URL)

def start_consumer():
    def _run():
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange='events', exchange_type='topic', durable=True)
        q = ch.queue_declare(queue='accounts_events', durable=True).method.queue
        ch.queue_bind(queue=q, exchange='events', routing_key='user.created')
        def callback(ch, method, properties, body):
            try:
                payload = json.loads(body)
                logging.info("Received event user.created %s", payload)
                handle_user_created(payload)
            except Exception as e:
                logging.exception("Event handler failed: %s", e)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.basic_consume(queue=q, on_message_callback=callback)
        ch.start_consuming()
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
