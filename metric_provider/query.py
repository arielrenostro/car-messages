import os
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Attr
from flask import json

from utils import get_unix_timestamp
from utils import decimal_encoder


def make_query(payload):
    date_range = payload['range']
    date_from = datetime.strptime(date_range['from'], '%Y-%m-%dT%H:%M:%S.%fZ')
    date_to = datetime.strptime(date_range['to'], '%Y-%m-%dT%H:%M:%S.%fZ')
    targets = []

    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.getenv('ACCESS_KEY'),
        aws_secret_access_key=os.getenv('SECRET_KEY'),
        region_name=os.getenv('REGION_NAME')
    )

    table = dynamodb.Table(
        os.getenv('DYNAMODB_TABLE')
    )

    fields = list(
        map(lambda x: x['target'], payload['targets'])
    )

    date_from_str = date_from.strftime("%Y/%m/%dT%H:%M:%S.%fZ")
    date_to_str = date_to.strftime("%Y/%m/%dT%H:%M:%S.%fZ")
    query = table.scan(
        FilterExpression=Attr('date').between(date_from_str, date_to_str),
        Limit=payload['maxDataPoints']
    )

    query = query['Items']
    for field in fields:
        target = {
            'target': field,
            'datapoints': [[item.get(field), get_unix_timestamp(item['date'])] for item in query]
        }
        target['datapoints'].sort(key=lambda x: x[1])
        targets.append(target)

    return json.dumps(targets, default=decimal_encoder)
