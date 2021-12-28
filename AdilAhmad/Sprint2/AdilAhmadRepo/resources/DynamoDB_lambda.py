import boto3


def lambda_handler(event, context):
    db = boto3.client("dynamodb")
    message = event['Records'][0]['Sns']['MessageId']
    time = event['Records'][0]['Sns']['Timestamp']
    alarmName = event['Records'][0]['Sns']['Subject']
    if message[0]=="B":
        table_name="Beta-adil2-stack-TableCD117FA1-6Y78TCR5HQCB"
    else:
        table_name="Prod-adil2-stack-TableCD117FA1-TBPT3DZT3SWC"
    db.put_item(TableName=table_name, Item={
        'id':{'S':message},
        'createdDate':{'S':time},
        'name':{'S':alarmName}
    })