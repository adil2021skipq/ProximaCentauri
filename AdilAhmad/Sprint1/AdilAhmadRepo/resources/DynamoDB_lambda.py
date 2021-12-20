import boto3
import os


def lambda_handler(event, context):
    db = boto3.client("dynamodb")
    message = event['Records'][0]['Sns']['MessageId']
    time = event['Records'][0]['Sns']['Timestamp']
    values = {}
    values['id'] = message
    values['createdDate'] = time
    db.put_item(TableName="AdilAhmadAlarmTable",
    Item = values)