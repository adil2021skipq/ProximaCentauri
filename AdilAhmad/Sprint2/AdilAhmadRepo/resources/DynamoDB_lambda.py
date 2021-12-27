# import boto3


# def lambda_handler(event, context):
#     db = boto3.client("dynamodb")
#     message = event['Records'][0]['Sns']['MessageId']
#     time = event['Records'][0]['Sns']['Timestamp']
#     alarmName = event['Records'][0]['Sns']['Subject']
#     if message[0]=="B":
#       table_name="Beta-adil-skip-stack-TableCD117FA1-AAV1AQC91TB1"
#     else:
#         table_name="Prod-adil-skip-stack-TableCD117FA1-129QCNZI6QH1U"
#     db.put_item(TableName=table_name, Item={
#         'id':{'S':message},
#         'createdDate':{'S':time},
#         'name':{'S':alarmName}
#     })