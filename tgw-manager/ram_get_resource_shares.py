import boto3

# test script to get the show all attachments of the transit gateway


ram = boto3.client('ram')

# get resources that can be shared.  Should know which is the resourceShareArn for the transit gateway
response = ram.get_resource_shares(
resourceOwner='SELF'
#Filters=[{'Name':'transit-gateway-id','Values':['tgw-07c16ca582c6fbee9']}]
)
print("get_resource_shares():")
print(response)

# what are invitations?  All outstanding only?  Seems to be outstanding - invitation sent but not accepted
response = ram.get_resource_share_invitations(
resourceShareArns=['arn:aws:ram:us-west-2:422384181506:resource-share/66b3c25a-7d35-b50b-720a-7a63065546f0']
)
print("get_resource_share_invitations():")
print(response)


# 
response = ram.get_resource_share_associations(
#associationType='PRINCIPAL',
associationType='RESOURCE',
resourceShareArns=['arn:aws:ram:us-west-2:422384181506:resource-share/66b3c25a-7d35-b50b-720a-7a63065546f0']
)
print("get_resource_share_associations():")
print(response)


