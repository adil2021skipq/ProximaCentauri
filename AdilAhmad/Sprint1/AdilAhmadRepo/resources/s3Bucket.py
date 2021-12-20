import aws_cdk.aws_s3 as s3 
import boto3

class bucket_s3():
    def __init__(self):
        bucket= s3.Bucket(self, "s3_bucket")
    
    # def read_file(self, bucket):
    #     name_url = []
    #     s3 = boto3.resource('s3')
    #     obj = s3.Object(bucket, key)
    #     for line in obj.get()['Body']._raw_stream.readline():
    #         name_url.append(line)
    #     return name_url