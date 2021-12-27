# import boto3


# def lambda_handler(event, context):
#     db = boto3.client("dynamodb")
#     message = event['Records'][0]['Sns']['MessageId']
#     time = event['Records'][0]['Sns']['Timestamp']
#     alarmName = event['Records'][0]['Sns']['Subject']
#     if message[0]=="B":
#         table_name="Beta-adil-stack-TableCD117FA1-9T5UV5HM0L7X"
#     else:
#         table_name="Prod-adil-stack-TableCD117FA1-584GC4KCY32C"
#     db.put_item(TableName=table_name, Item={
#         'id':{'S':message},
#         'createdDate':{'S':time},
#         'name':{'S':alarmName}
#     })