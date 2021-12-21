import boto3

def get_urls():
    client = boto3.client('s3')
    response = client.get_object(Bucket="adilahmadrepostack-adilahmadbuckete333b1d5-71bp3yb189i0", 
    )