import boto3 , json

def ReadFromTable(tableName):
    db = boto3.client('dynamodb')
    
    Urls = db.scan(TableName=tableName,AttributesToGet=['Links'])
    links = Urls['Items'] 
    
    URL_names = {}
    for i in range(len(links)):
        URL_names[i] = links[i]
     
    names = []
    for j in range(len(URL_names)):
       names.append(URL_names[j]['Links']['S'])
    return names