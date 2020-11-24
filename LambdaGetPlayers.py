import json
import boto3
import decimal
import datetime
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('getPlayerID')
    return {
        'statusCode': 200,
        'body': json.dumps(table.scan(), cls=JsonIntEncoder)
    }

class JsonIntEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(JsonIntEncoder, self).default(obj)