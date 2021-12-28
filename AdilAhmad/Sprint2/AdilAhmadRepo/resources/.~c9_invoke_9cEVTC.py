import boto3


def lambda_handler(event, context):
    db = boto3.client("dynamodb")
    message = event['Records'][0]['Sns']['MessageId']
    time = event['Records'][0]['Sns']['Timestamp']
    alarmName = event['Records'][0]['Sns']['Subject']
    table_name=os.getenv('table_name')
    db.put_item(TableName=table_name, Item={
        'id':{'S':message},
        'createdDate':{'S':time},
        'name':{'S':alarmName}
    })