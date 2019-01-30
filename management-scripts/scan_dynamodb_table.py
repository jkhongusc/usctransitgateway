import boto3

# test script to get the states of the VPN tunnels
# VPN state should be active
# two VPN tunnels should be UP


ddb = boto3.client('dynamodb')
response = ddb.scan(
TableName='dynamodb-tgw-table'
)
print(response)
