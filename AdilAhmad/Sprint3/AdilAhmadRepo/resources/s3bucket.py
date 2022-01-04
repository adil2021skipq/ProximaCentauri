import json
import boto3


class S3Bucket:
    def __init__(self, buck):
        self.bucket = boto3.resource("s3", region_name='us-east-2').Bucket(buck)

    def load(self, key):
        return json.load(self.bucket.Object(key=key).get()["Body"])
        
    def dump(self, key, obj):
        return self.bucket.Object(key=key).put(Body=json.dumps(obj))