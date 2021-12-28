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
    aws_codedeploy as codedeploy,
    
)
from resources import constants as constants
import boto3, json
from resources.s3bucket import S3Bucket as s3b

class AdilAhmadRepoStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role=self.create_lambda_role()
        Hwlambda=self.create_lambda("HelloLambda", "./resources", "webhealth_lambda.lambda_handler", lambda_role)
        DBlambda=self.create_lambda("DynamoDBLambda", "./resources", "DynamoDB_lambda.lambda_handler", lambda_role)
        
        lambda_schedule=events_.Schedule.rate(cdk.Duration.minutes(1)) 
        lambda_targets= targets_.LambdaFunction(handler=Hwlambda)
        rule=events_.Rule(self, "webhealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
        
        # d = boto3.client("dynamodb")
        # dnm = boto3.resource("dynamodb")
        # response=d.list_tables()
        # if ("AdilAhmadAlarmTable" in response["TableNames"]):
        # dynamo_table=self.create_table()
        # else:
        
        
        dynamo_table=self.create_table()
        dynamo_table.grant_read_write_data(DBlambda)
        DBlambda.add_environment('table_name', dynamo_table.table_name)

        topic = sns.Topic(self, "WebHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription(email_address="adil.ahmad.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=DBlambda))
        
        
        # bucket = s3_.Bucket(self, id="AdilBucket")
        
        
        # s3 = boto3.resource('s3')
        # object = s3.Object('adilbucket','urls.json')
        # response = object.put(Body=json.dumps({
        #         "URLS": [
        #     {
        #     "FACEBOOK": "www.facebook.com",
        #     "TWITTER": "www.twitter.com",
        #     "ESPNCRICINFO": "www.espncricinfo.com",
        #     "REDDIT": "www.reddit.com",
        #     }
        # ]
        # }))
        
        
        URLS = s3b('beta-adil2-stack-adilbucketd08c6c2a-hv2jjjpyare0').load('urls.json')
        K=list(URLS['URLS'][0].keys())
        
        availability_metric = []
        latency_metric = []
        
        for i in range(len(K)):
            
            dimensions = {'URL': URLS['URLS'][0][K[i]]}
            availability_metric.append(
                                cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                                metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                                dimensions_map = dimensions,
                                period = cdk.Duration.minutes(5),
                                label = f'{K[i]} Availability Metric')
                                )
                        
            latency_metric.append(
                                cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                                metric_name=constants.URL_MONITOR_NAME_LATENCY,
                                dimensions_map = dimensions,
                                period = cdk.Duration.minutes(1),
                                label = f'{K[i]} Latency Metric')
                                )

        availability_alarm = []
        latency_alarm = []
        
        for i in range(len(K)):
            
            availability_alarm.append(
                                    cloudwatch_.Alarm(self, 
                                    id = f'Adil Ahmad_{K[i]}_Availability_Alarm',
                                    alarm_description = f"Alarm to monitor availability of {K[i]}",
                                    metric = availability_metric[i],
                                    comparison_operator =cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                                    datapoints_to_alarm = 1,
                                    evaluation_periods = 1,
                                    threshold = 1)
                                    )
                                    
            latency_alarm.append(
                                    cloudwatch_.Alarm(self, 
                                    id = f'Adil Ahmad_{K[i]}_Latency_Alarm',
                                    alarm_description = f"Alarm to monitor latency of {K[i]}",
                                    metric = latency_metric[i],
                                    comparison_operator =cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                    datapoints_to_alarm = 1,
                                    evaluation_periods = 1,
                                    threshold = 0.245)
                                )
        for i in range(len(K)):
            
            availability_alarm[i].add_alarm_action(cw_actions.SnsAction(topic))
            latency_alarm[i].add_alarm_action(cw_actions.SnsAction(topic))
            
        metricduration = cloudwatch_.Metric(namespace="AWS/Lambda", metric_name="Duration", 
            dimensions_map={"FunctionName": DBlambda.function_name})
        failure_alarm = cloudwatch_.Alarm(self, "DurationAlarm", metric=metricduration, threshold = 700,
            comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            evaluation_periods=1)
        DBalias = lambda_.Alias(self, id = "AdilAlias "+construct_id, alias_name="AdilAlias", version=DBlambda.current_version)
        codedeploy.LambdaDeploymentGroup(self, "AdilID", alias=DBalias, alarms=[failure_alarm])
        
        
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by=aws_iam.CompositePrincipal(
                                    aws_iam.ServicePrincipal("lambda.amazonaws.com"),
                                    aws_iam.ServicePrincipal("sns.amazonaws.com"),
                                    aws_iam.ServicePrincipal('codebuild.amazonaws.com')
                        ),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"), 
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess")
            ]
        )
        return lambdaRole
        
    def create_lambda(self, newid, asset, handler, role):
        return lambda_.Function(self, id=newid, 
        runtime=lambda_.Runtime.PYTHON_3_8, 
        handler=handler, 
        code=lambda_.Code.from_asset(asset),
        role=role,
        timeout= cdk.Duration.minutes(5)
        )
        
    def create_table(self):
        return db.Table(self, 
        id="Table",
        partition_key=db.Attribute(name="id", type=db.AttributeType.STRING),
        sort_key=db.Attribute(name="createdDate", type=db.AttributeType.STRING)
        )
# Random Comment-10