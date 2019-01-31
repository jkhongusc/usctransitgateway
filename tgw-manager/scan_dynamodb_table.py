import boto3

# prints out all the items from the DynamoDB table


ddb = boto3.client('dynamodb')
response = ddb.scan(
TableName='dynamodb-tgw-table'
)
print(response)
