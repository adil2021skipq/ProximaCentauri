from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as cw_actions,
    aws_dynamodb as db,
    aws_s3 as s3_,
    aws_s3_notifications as s3n,
    aws_sqs as sqs_,
)
from resources import constants as constants
import boto3

class AdilAhmadRepoStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role=self.create_lambda_role()
        table_role=self.create_db_lambda_role()
        Hwlambda=self.create_lambda("HelloLambda", "./resources", "webhealth_lambda.lambda_handler", lambda_role)
        DBlambda=self.create_lambda("DynamoDBLambda", "./resources", "DynamoDB_lambda.lambda_handler", table_role)
        
        lambda_schedule=events_.Schedule.rate(cdk.Duration.minutes(1)) 
        lambda_targets= targets_.LambdaFunction(handler=Hwlambda)
        rule=events_.Rule(self, "webhealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
        
        d = boto3.client("dynamodb")
        dnm = boto3.resource("dynamodb")
        response=d.list_tables()
        if ("AdilAhmadAlarmTable" in response["TableNames"]):
            dynamo_table=dnm.Table('AdilAhmadAlarmTable')
        else:
            dynamo_table=self.create_table()
        
        topic = sns.Topic(self, "WebHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription(email_address="adil.ahmad.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=DBlambda))
        
        dimensions={"URL": constants.URL_TO_MONITOR, "Region": "DUB"}
        availability_metric=cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE, 
        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY, 
        dimensions_map=dimensions, 
        period=cdk.Duration.minutes(1),
        label="Availability Metric"
        )
        availability_alarm=cloudwatch_.Alarm(self, 
            id="AvailabilityAlarm", 
            metric=availability_metric,
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods=1,
            threshold=1
        )
    
        dimensions={"URL": constants.URL_TO_MONITOR, "Region": "DUB"}
        latency_metric=cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,
        metric_name=constants.URL_MONITOR_NAME_LATENCY, 
        dimensions_map=dimensions,
        period=cdk.Duration.minutes(1),
        label="Latency Metric"
        )
        latency_alarm=cloudwatch_.Alarm(self, 
            id="LatencyAlarm", 
            metric=latency_metric,
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods=1,
            threshold=0.245
        )    
        
        availability_alarm.add_alarm_action(cw_actions.SnsAction(topic))
        latency_alarm.add_alarm_action(cw_actions.SnsAction(topic))
        
        bucket=s3_.Bucket(self, "Bucket")
        queue=sqs_.Queue(self, "Queue", visibility_timeout=cdk.Duration.seconds(250))
        bucket.add_event_notification( s3_.EventType.OBJECT_CREATED, s3n.SqsDestination(queue))
        
        
    def create_lambda_role(self):
        lambdaRole=aws_iam.Role(self, "lambda-role",
        assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),            
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess")
            ]
        )
        return lambdaRole
        
    def create_lambda(self, newid, asset, handler, role):
        return lambda_.Function(self, id=newid, 
        runtime=lambda_.Runtime.PYTHON_3_8, 
        handler=handler, 
        code=lambda_.Code.from_asset(asset),
        role=role
        )
        
    def create_table(self):
        return db.Table(self, 
        id="Table", 
        table_name="AdilAhmadAlarmTable", 
        partition_key=db.Attribute(name="id", type=db.AttributeType.STRING)
        )
        
    def create_db_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess')
                        ])
        return lambdaRole