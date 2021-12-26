import pytest
from aws_cdk import core
from adil_ahmad_repo.adil_ahmad_repo_stack import AdilAhmadRepoStack

def test_lambda():
    app = core.App()
    
    AdilAhmadRepoStack(app, "Stack")
    template = app.synth().get_stack_by_name("Stack").template
    functions = [resource for resource in template["Resources"].values() if resource["Type"] == "AWS::Lambda::Function"]
    
    assert len(functions) == 2
