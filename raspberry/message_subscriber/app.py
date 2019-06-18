import json
import os

import pika

from raspberry.message_subscriber.car_controller import turn_car_on


def handle_consume(ch, method, properties, body):
    print(f"Message received: {body}")
    try:
        message = json.loads(body)
        if 'action' in message:
            action = message['action']
            if 'TURN-ON' == action:
                turn_car_on()
            else:
                print(f"Invalid action '{action}'")
        else:
            print(f"Message don't have 'action' field")
    except Exception as e:
        print(f"Error to process message. {e}")
    else:
        print(f"Message processed")


while True:
    print("Starting connection...")
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST'),
            port=int(os.getenv('RABBITMQ_PORT', '5672')),
        )
    )

    channel = connection.channel()

    print("Declaring queue...")
    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))

    channel.basic_consume(
        queue=os.getenv('RABBITMQ_QUEUE'),
        auto_ack=True,
        on_message_callback=handle_consume
    )

    print("Waiting for message...")
    channel.start_consuming()
