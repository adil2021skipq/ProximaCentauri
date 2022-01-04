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

from adil_ahmad_repo.adil_ahmad_repo_stack import AdilAhmadRepoStack

class Pipeline_Stage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        infra_stack = AdilAhmadRepoStack(self, "adil2-stack")