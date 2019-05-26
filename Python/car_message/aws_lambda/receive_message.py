import json
import os
from datetime import datetime
from decimal import Decimal

import boto3


def lambda_handler(event, context):
    body = get_body(event)

    count = 0
    if isinstance(body, (list, set)):
        for data in body:
            put_data(data)
            count += 1
    else:
        put_data(body)
        count += 1

    return {
        'statusCode': 200,
        'body': json.dumps({
            'count': count
        })
    }


def put_data(body):
    data = {
        'date': body.get('datetime', datetime.utcnow().strftime("%Y/%m/%dT%H:%M:%SZ")),
        'car': body.get('car'),
        'speed': get_decimal(body, 'speed'),
        'rpm': get_decimal(body, 'rpm'),
        'intake_temp': get_decimal(body, 'intakeTemperature'),
        'oil_temp': get_decimal(body, 'oilTemperature'),
        'coolant_temp': get_decimal(body, 'coolantTemperature'),
        'latitude': get_decimal(body, 'latitude'),
        'longetude': get_decimal(body, 'longetude'),
    }

    data.update({
        'id': f'{data["car"]}_{data["date"]}'
    })

    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=os.getenv('ACCESS_KEY'),
            aws_secret_access_key=os.getenv('SECRET_KEY'),
        )

        table = dynamodb.Table(
            os.getenv('DYNAMODB_TABLE')
        )

        table.put_item(
            Item=data
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'message': str(e)
            }
        }


def get_body(event):
    if 'body' in event:
        body = event['body']
        if isinstance(body, str):
            return json.loads(body)
        elif isinstance(body, dict):
            return body
    return {}


def get_decimal(body, key):
    if key in body:
        value = body[key]
        try:
            return Decimal(
                str(value)
            )
        except:
            pass


def parse_value_json_data(value):
    if isinstance(value, Decimal):
        return str(value)
    return value
