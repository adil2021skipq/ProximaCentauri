from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
)

class AdilAhmadRepoStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role=self.create_lambda_role()
        Hwlambda=self.create_lambda("HelloLambda", "./resources", "webhealth_lambda.lambda_handler", lambda_role)
        lambda_schedule=events_.Schedule.rate(cdk.Duration.minutes(1)) 
        lambda_targets= targets_.LambdaFunction(handler=Hwlambda)
        rule=events_.Rule(self, "webhealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
    
    def create_lambda_role(self):
        lambdaRole=aws_iam.Role(self, "lambda-role",
        assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
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