import boto3

# test script to get the states of the VPN tunnels
# VPN state should be active
# two VPN tunnels should be UP

ec2 = boto3.client('ec2')
#response = ec2.describe_instances()
response = ec2.describe_vpn_connections()
#print(response)

tunnels = response['VpnConnections']

for tunnel in tunnels:
#    if tunnel['State'] == 'available':
#          num_connections += 1
#          active_tunnels = 0
#          if tunnel['VgwTelemetry'][0]['Status'] == 'UP':
#              active_tunnels += 1
#          if tunnel['VgwTelemetry'][1]['Status'] == 'UP':
#              active_tunnels += 1
    print (tunnel['VpnConnectionId'])
#      print (return_value(tunnel['Tags'], 'Name'))
    print ("  " + tunnel['State'])
    print ("    " + tunnel['VgwTelemetry'][0]['Status'])
    print ("    " + tunnel['VgwTelemetry'][1]['Status'])
    print (" ")
