import boto3

# test script to get the show all attachments of the transit gateway


ec2 = boto3.client('ec2')
#response = ec2.describe_instances()
#response = ec2.describe_vpn_connections()
response = ec2.describe_transit_gateway_attachments(
Filters=[{'Name':'transit-gateway-id','Values':['tgw-07c16ca582c6fbee9']}]
)
print(response)
