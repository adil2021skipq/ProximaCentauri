# Welcome to my CI/CD Pipeline Program

## Objective 

> <em> The objective of this program is to deploy the web health application developed earlier through a CI/CD Pipeline </em>

## AWS Modules Utilized

> * S3
> * DynamoDB
> * IAM
> * Cloud9
> * CloudFormation
> * CloudWatch
> * SecretsManager
> * Lambda
> * CodeBuild
> * SNS

## How to run this program

### Clone the repository

> ` git clone https://github.com/adil2021skipq/ProximaCentauri.git `  

### Go to the required directory

> ` cd AdilAhmad/Sprint2/AdilAhmadRepo `

### Bootstrap the environment

> ` cdk bootstrap aws://315997497220/us-east-2 --qualifier adil --toolkit-stack adil2-toolkit `

### Deploy the pipeline

> ` cdk deploy AdilSkip3Pipeline `


# Author: Adil Ahmad