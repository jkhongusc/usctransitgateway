# usctransitgateway::monitor::monitortgwresourceshares
Checks the customer list from the DynamoDb table dynamodb-tgw-table. Compares the list from dynamodb to what is actually connected. Actual connections are gathered from transit gateway attachments (actual connections) and the resource access manager (shares/invitations).

There is a gap in functionality.  The AWS spoke account has to attach their VPC to the transit gateway.  This function which runs on the hub/master account cannot make the spoke VPC attachment.  Possible but requires a lot of work with assumed roles


Describe functionality (TBD)
- inputs (event): 
  - REGION - AWS region
  - TRANSITGATEWAY - list of transit gateways (ids) to monitor
  - RAMSHARENAME ram share name
- inputs (os): 
  - SLACKTOKEN - slack token, careful not to check-in code with token
  - SLACKNAME - name of bot/user
  - SLACKCHANNEL - slack channel name
- Error condition if:
- outputs:
  - CloudWatch logs
  - Slack Channel

## environment
- Environment was created using virtualenv:
  - virtualenv monitortgwresourceshares
  - cd monitortgwresourceshares/bin
  - source activate
  - pip install slackclient
  - deactivate

- Environment was created manually:
  - mkdir monitortgwresourceshares
  - cd monitortgwresourceshares
  - pip install slackclient --target .


## EC2 testing
To run (lambda) function on EC2:
python3 commandline.py



## deployment
To create deployment (zip) file:

cd monitortgwresourceshares

./create_zip.sh


Copy deployment script to an S3 bucket:

aws s3 cp monitortgwresourceshares.zip s3://tgw-us-west-2-public/monitortgwresourceshares.zip


## CloudFormation Template
[monitortgwresourceshares.yaml](monitortgwresourceshares.yaml) - CFT that creates these AWS resources to deploy as lambda function:
- IAM lambda role: 
  - AmazonEC2ReadOnlyAccess: EC2 read-only
  - AWSLambdaBasicExecutionRole: lambda basic execution
  - S3 read/get access
- Lambda function


## lambda configuration
load code from S3 - https://s3.amazonaws.com/tgw-us-west-2-public/monitortgwresourceshares.zip

Runtime: Python 3.7

Handler: main.lambda_handler

Environment variables (required): SLACKCHANNEL, SLACKNAME, SLACKTOKEN

role: requires policies - AmazonEC2ReadOnlyAccess, AWSLambdaBasicExecutionRole

Memory: 128MB

Timeout: 1min

Network: No VPC

Configure test events (example configuration):
{
  "REGION": "us-west-2",
  "VPN": [
    "vpn-01234567890",
    "vpn-01dd07c2c43662ff0"
  ]
}


## suggested improvements
- Error handling - Exception be thrown for any error
- code cleanup
- Microsoft Teams bot- add notification via Teams
- Handle multiple transit gateways - lower priority
- 

## comments
- EC2 boto3:
  - describe_transit_gateway_vpc_attachments() - [Useful] Returns a list of all VPC attachments to the transit gateway
- RAM boto3:
  - list_principals() - [Useful] Returns a list of all the principals (AWS accounts) that are connected (accepted) to the resource (transit gateway)
  - create_resource_share() - [Useful] Use to create a resource share (invitation) of the transit gateway to a spoke account
  - get_resource_share_invitations() - [Not useful] Appears to be share invitations to the hub account, not shares sent from the hub account. The latter is useful for monitoring purposes.
  - get_resource_share_associations() - [Not useful] Returns a list of resource shares but no useful information is returned.  Useful information would be AWS account, resource type, resource id.

