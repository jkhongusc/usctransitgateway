from main import lambda_handler
import os

# hard code input to lambda function
event ={}
event['REGION'] = 'us-west-2'
event['TRANSITGATEWAY'] = [ 'tgw-0140bb4dfd328a656' ]
event['RAMSHARENAME'] = [ 'its-tgw-auto-us-west-2' ]

#os.environ['SLACKTOKEN'] = ''
os.environ['SLACKNAME'] = 'aws_notifications'
os.environ['SLACKCHANNEL'] = 'uschomepageadmin'


lambda_handler(event,None)




