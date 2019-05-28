from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key
from flask import json

from utils import get_unix_timestamp


def make_query(payload):
    date_range = payload['range']
    date_from = datetime.strptime(date_range['from'], '%Y-%m-%dT%H:%M:%S.%fZ')
    date_to = datetime.strptime(date_range['to'], '%Y-%m-%dT%H:%M:%S.%fZ')
    targets = []
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Car')
    fields = list(map(lambda x: x['target'], payload['targets']))
    query = table.query(
        AtributesToGet=[*fields, 'date'],
        KeyConditionExpression=Key('date').between(date_from, date_to),
        Limit=payload['maxDataPoints']
    )
    query = query['Items']
    for field in fields:
        target = {
            'target': field,
            'datapoints': [[item['field'], get_unix_timestamp(item['date'])] for item in query]
        }

        targets.append(target)
    return json.dumps(targets)
