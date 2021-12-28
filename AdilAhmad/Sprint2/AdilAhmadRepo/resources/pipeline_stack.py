from aws_cdk import core
from aws_cdk import pipelines
from aws_cdk import aws_iam
from aws_cdk import aws_codepipeline_actions as cpactions
from resources.pipeline_stage import Pipeline_Stage

class MyPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        source = pipelines.CodePipelineSource.git_hub(repo_string="adil2021skipq/ProximaCentauri", branch="main",
        authentication=core.SecretValue.secrets_manager("adil-github-token"),
        trigger=cpactions.GitHubTrigger.POLL)
        
        # synth = pipelines.ShellStep("synth", input = source,
        # commands = ["cd AdilAhmad/Sprint2/AdilAhmadRepo", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
        # primary_output_directory = "AdilAhmad/Sprint2/AdilAhmadRepo/cdk.out")
        
        pipelineroles = self.createrole()
        
        synth = pipelines.CodeBuildStep('synth',input=source,
        commands=["cd AdilAhmad/Sprint2/AdilAhmadRepo","pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
        primary_output_directory="AdilAhmad/Sprint2/AdilAhmadRepo/cdk.out",
        role=pipelineroles
        )
        
        pipeline = pipelines.CodePipeline(self, "Pipeline", synth = synth)
        
        beta = Pipeline_Stage(self, "Beta",
        env={
            "account":"315997497220",
            "region":"us-east-2"
        })
        
        prod = Pipeline_Stage(self, "Prod",
        env={
            "account":"315997497220",
            "region":"us-east-2"
        })
        
        # unit_test = pipelines.ShellStep("unit_test",
        # commands = ["cd AdilAhmad/Sprint2/AdilAhmadRepo", "pip install -r requirements.txt", "pytest unit", "pytest integ"]
        # )
        
        unit_test = pipelines.CodeBuildStep('unit_test',
        commands=["cd AdilAhmad/Sprint2/AdilAhmadRepo","pip install -r requirements.txt", "npm install -g aws-cdk", "pytest unit", "pytest integ"],
        role=pipelineroles
        )
        
        pipeline.add_stage(beta, 
        pre = [unit_test])
        pipeline.add_stage(prod,
        pre=[
            pipelines.ManualApprovalStep("PromoteToProd")    
        ])
    
    def createrole(self):
        role=aws_iam.Role(self,"pipeline-role",
        assumed_by=aws_iam.CompositePrincipal(
            aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            aws_iam.ServicePrincipal("sns.amazonaws.com"),
            aws_iam.ServicePrincipal('codebuild.amazonaws.com')
            ),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AwsCloudFormationFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipeline_FullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ])
        return role 