import boto3
import constants as constants

class cloudwatchPutMetric:
    def __init__(self):
        self.client=boto3.client("cloudwatch")

    def put_data(self, nameSpace, metricname, dimensions, value):
        response=self.client.put_metric_data(
            Namespace=nameSpace,
            MetricData=[
                {
                "MetricName":metricname,
                "Dimensions":dimensions,
                "Value":value,
            },
            ])
        