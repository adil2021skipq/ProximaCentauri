from aws_cdk import core
from aws_cdk import pipelines
from aws_cdk import aws_codepipeline_actions as cpactions
from pipeline_stage import Pipeline_Stage

class MyPipelineStack(core.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        source = pipelines.CodePipelineSource.git_hub(repo_string="adil2021skipq/ProximaCentauri", branch="main",
        authentication=core.SecretValue.secrets_manager("adil-github-token"),
        trigger=cpactions.GitHubTrigger.POLL)
        
        synth = pipelines.ShellStep("synth", input = source,
        commands = ["AdilAhmad/Sprint2/AdilAhmadRepo", "pip install -r requirements.txt -t ./AdilAhmadRepo/resouces/dependencies", "npm install -g aws-cdk", "cdk synth"],
        primary_output_directory = "AdilAhmad/Sprint2/AdilAhmadRepo/cdk.out")
        
        pipeline = pipelines.CodePipeline(self, "Pipeline", synth = synth)
        
        beta = Pipeline_Stage(self, "beta")
        
        pipeline.add_stage(beta)
        
        # pipeline = pipelines.CodePipeline(self, "Pipeline",
        #     synth=pipelines.ShellStep("Synth",
        #         # Use a connection created using the AWS console to authenticate to GitHub
        #         # Other sources are available.
        #         input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
        #             connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
        #         ),
        #         commands=["npm ci", "npm run build", "npx cdk synth"
        #         ]
        #     )
        # )

        # # 'MyApplication' is defined below. Call `addStage` as many times as
        # # necessary with any account and region (may be different from the
        # # pipeline's).
        # pipeline.add_stage(MyApplication(self, "Prod",
        #     env=cdk.Environment(
        #         account="123456789012",
        #         region="eu-west-1"
        #     )
        # ))