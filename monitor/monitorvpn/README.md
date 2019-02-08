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
cd monitorvpn/lib/python3.7/site-packages

zip -r9 ../../../../mylambda.zip *

zip -g mylambda.zip main.py

aws s3 cp mylambda.zip https://s3.amazonaws.com/jkhong-test-public/mylambda.zip


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
