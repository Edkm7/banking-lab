import pika
from .config import settings
import json

params = pika.URLParameters(settings.RABBITMQ_URL)

def publish(exchange: str, routing_key: str, body: dict):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(body))
    connection.close()
