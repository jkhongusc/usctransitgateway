from main import lambda_handler

# hard code input to lambda function
event ={}
event['REGION'] = 'us-west-2'
event['TRANSITGATEWAY'] = [ 'tgw-0140bb4dfd328a656' ]

lambda_handler(event,None)




