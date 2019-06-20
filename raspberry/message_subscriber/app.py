import json
import os

import car_controller as car
import mq


def handle_consume(ch, method, properties, body):
    print(f"Message received: {body}")

    try:
        message = json.loads(body)
        action = message.get('action')

        if not action:
            print(f"Message don't have 'action' field")
            return

        if 'TURN-ON' == action:
            car.turn_on()

        else:
            print(f"Invalid action '{action}'")

    except Exception as e:
        print(f"Error to process message. {e}")
    finally:
        print(f"Message processed")


try:
    car.init()
    mq.init()

    mq.channel.basic_consume(
        queue=os.getenv('RABBITMQ_QUEUE'),
        auto_ack=True,
        on_message_callback=handle_consume,
    )

    print("Waiting for message...")
    mq.channel.start_consuming()
finally:
    car.stop()
    mq.stop()
