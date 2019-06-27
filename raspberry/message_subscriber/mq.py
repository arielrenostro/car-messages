import json
import os
from datetime import datetime

import pika


connection = None
channel = None


def init():
    global connection
    global channel

    print("Starting consumer connection...")
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST'),
            port=int(os.getenv('RABBITMQ_PORT', '5672')),
        )
    )

    channel = connection.channel()

    print("Declaring queue...")
    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))
    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE_RESPONSE'))


def stop():
    if connection:
        connection.close()


def send_info_message(message, action=None):
    body = _make_body(message, action, 'INFO')
    print(body)
    return _send_message(body)


def send_error_message(message, action=None):
    body = _make_body(message, action, 'ERROR')
    print(body)
    return _send_message(body)


def _send_message(message):
    return channel.basic_publish(
        exchange='',
        routing_key=os.getenv('RABBITMQ_QUEUE_RESPONSE'),
        body=message
    )


def _make_body(message, action, type_):
    return json.dumps({
        'action': action,
        'date': datetime.utcnow().strftime("%Y/%m/%dT%H:%M:%S.%fZ"),
        'message': message,
        'type': type_,
    })
