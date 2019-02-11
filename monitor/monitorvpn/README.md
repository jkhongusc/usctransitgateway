# usctransitgateway::monitor::monitorvpn 
Monitors VPN connections

Describe functionality (TBD)
- inputs: 
  - region
  - list of VPN (ids) to monitor
- Error condition if:
  - VPN is not found
  - VPN state is not 'available'
  - VPN tunnels are 'DOWN' or not 'UP'
- outputs:
  - CloudWatch logs
  - Slack Channel

## environment
Environment was created using virtualenv:

virtualenv monitorvpn

cd monitorvpn/bin

source activate

pip install slackclient


## deployment
To create deployment (zip) file:

cd monitorvpn

./create_zip.sh


Copy deployment script to an S3 bucket:

aws s3 cp monitorvpn.zip https://s3.amazonaws.com/jkhong-test-public/monitorvpn.zip


## CloudFormation Template
[monitorvpn.yaml](monitorvpn.yaml) - CFT that creates these AWS resources to deploy as lambda function:
- IAM lambda role: 
  - AmazonEC2ReadOnlyAccess: EC2 read-only
  - AWSLambdaBasicExecutionRole: lambda basic execution
  - S3 read/get access
- Lambda function


## lambda configuration
load code from S3

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
- Error handling - should an Exception be thrown for any error
- code cleanup
- Microsoft Teams bot- add notification via Teams
- 

