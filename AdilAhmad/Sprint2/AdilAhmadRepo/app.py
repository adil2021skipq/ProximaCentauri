#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from aws_cdk import core

from resources.pipeline_stack import MyPipelineStack

app = core.App()

MyPipelineStack(app, "AdilSkip1Pipeline", env = cdk.Environment(account="315997497220", region="us-west-2"))
app.synth()
