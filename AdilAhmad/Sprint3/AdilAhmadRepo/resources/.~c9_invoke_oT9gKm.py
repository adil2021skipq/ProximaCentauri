import boto3,os
import read_table 
from s3bucket import S3Bucket as s3b
db = boto3.client('dynamodb')


def lambda_handler(events, context):
    db = boto3.client('dynamodb')
    
    
    URLS= s3b('AdilBucket').load('urls.json')
    
    urltable = os.getenv(key = 'table_name')
    
    for link in URLS:
        db.put_item(TableName = urltable,Item=
        {
            'Links':{'S': link}
        })
    
    
    
    method = events['httpMethod']
    
    if method == 'GET':
        data = read_table.ReadFromTable(urltable)
        response = f"URLS = {data} "
    
    elif method == 'PUT':
        new_url = events['body']
        db.put_item(
        TableName = urltable,
        Item={
        'Links':{'S' : new_url},
        })
        response = f"Url = {events['body']} is successfully added into the table"
        
    elif method == 'DELETE':
        new_url = events['body']
        db.delete_item(
        TableName =urltable,
        Key={
        'Links':{'S' : new_url}
        })
        response = f"Url= {events['body']} is successfully deleted from the table"
        
    else:
        
        response = 'Indefinite Method Request Error.'
    print(response) 
    
    return {
        'statusCode' : 200,
        'body'  :  response
    }





































