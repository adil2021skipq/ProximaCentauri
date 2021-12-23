from aws_cdk import core
from aws_cdk import pipelines
from aws_cdk import aws_codepipeline_actions as cpactions
from resources.pipeline_stage import Pipeline_Stage

class MyPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        source = pipelines.CodePipelineSource.git_hub(repo_string="adil2021skipq/ProximaCentauri", branch="main",
        authentication=core.SecretValue.secrets_manager("adil-github-token"),
        trigger=cpactions.GitHubTrigger.POLL)
        
        synth = pipelines.ShellStep("synth", input = source,
        commands = ["cd AdilAhmad/Sprint1/AdilAhmadRepo", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
        primary_output_directory = "AdilAhmad/Sprint1/AdilAhmadRepo/cdk.out")
        
        pipeline = pipelines.CodePipeline(self, "Pipeline", synth = synth)
        
        beta = Pipeline_Stage(self, "Beta",
        env={
            "account":"315997497220",
            "region":"us-east-2"
        })
        
        pipeline.add_stage(beta)