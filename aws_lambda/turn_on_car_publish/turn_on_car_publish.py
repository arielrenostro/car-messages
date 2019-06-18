import json
import os
from datetime import datetime

import pika


def lambda_handler(event, context):
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST'),
            port=int(os.getenv('RABBITMQ_PORT', '5672')),
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))

    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('RABBITMQ_QUEUE'),
        body=json.dumps({
            'action': 'TURN-ON',
            'date': datetime.utcnow().strftime("%Y/%m/%dT%H:%M:%S.%fZ")
        })
    )

    connection.close()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Message published'
        })
    }


if __name__ == '__main__':
    lambda_handler(None, None)
