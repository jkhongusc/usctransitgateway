'''
To use this blueprint, your function's role must have permissions
to call ec2:DescribeRegions and ec2:DescribeVpnConnections.
For these permissions, you must specify "Resource": "*".

Example:
{
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "Stmt1443036478000",
        "Effect": "Allow",
        "Action": [
            "ec2:DescribeRegions",
            "ec2:DescribeVpnConnections"
        ],
        "Resource": "*"
    }]
}
'''

from __future__ import print_function

import boto3

from dynamodb import TgwDynamoDb
from ram import TgwRam

print('Loading function')
cw = boto3.client('cloudwatch')



def lambda_handler(event, context):
    # check to make sure all required parameters are defined
    #if 'SLACKTOKEN' not in os.environ:
    #    raise Exception('SLACKTOKEN environment variable not set')
    #if 'SLACKNAME' not in os.environ:
    #    raise Exception('SLACKNAME environment variable not set')
    #if 'SLACKCHANNEL' not in os.environ:
    #    raise Exception('SLACKCHANNEL environment variable not set')

    if 'REGION' not in event:
        raise Exception('REGION event variable not set')
    if 'TRANSITGATEWAY' not in event:
        raise Exception('TRANSITGATEWAY event variable not set')

    #stoken=os.environ['SLACKTOKEN']
    #sname=os.environ['SLACKNAME']
    #schannel=os.environ['SLACKCHANNEL']
    region=event['REGION']
    tgws=event['TRANSITGATEWAY']

    #slack_client = SlackClient(stoken)
    #slack_client.api_call( "chat.postMessage", channel=schannel, text="test from EC2")
    
    try:
        #ec2 = boto3.client('ec2',region_name=region)
        #response = ec2.describe_vpn_connections()
        print ("starting")
        myram = TgwRam(region)
        ramprincipals = myram.get_principals()
        mydynamo = TgwDynamoDb(region)
        print("Transit Gateway, (%d) Principals, " % (len(ramprincipals)) )
        tgwlist = mydynamo.get_transit_gateway() 
        vpclist = mydynamo.get_vpc() 
        vpnlist = mydynamo.get_vpn() 
        #print ("\n")
        print("(%d) Transit Gateway, (%d) VPCs, (%d) VPNs" % (len(tgwlist),len(vpclist),len(vpnlist)) )
        for tgwitem in tgwlist:
            print("Transit Gateway (%s) CIDR (%s)" % (tgwitem['TransitGatewayId'],tgwitem['Cidr']) )
        #print ("\n")
        for vpcitem in vpclist:
            print("    VPC (%s) CIDR (%s)" % (vpcitem['ResourceId'],vpcitem['Cidr']) )
        #print ("\n")
        for vpnitem in vpnlist:
            print("    VPN (%s) CIDR (%s)" % (vpnitem['ResourceId'],vpnitem['Cidr']) )
        
        
        '''
        for monitor_tgw in tgws:
            print( "processing "+monitor_tgw)
            if not any(vpn['VpnConnectionId'] == monitor_tgw for vpn in tgws):
                print( "[ERROR] "+monitor_tgw+" not found")
                #slack_client.api_call( "chat.postMessage", channel=schannel, text="[ERROR] "+monitor_tgw+" not found")
                continue
            for vpn in tgws:
                if (vpn['VpnConnectionId'] != monitor_tgw):
                    print ("skipping: "+vpn['VpnConnectionId'])
                    continue
                if (vpn['State'] != 'available' or vpn['VgwTelemetry'][0]['Status'] != 'UP' or
                    vpn['VgwTelemetry'][1]['Status'] != 'UP'): 
                    # error
                    print( "[ERROR] "+vpn['VpnConnectionId']+" is "+vpn['State']+"; tunnels: "+vpn['VgwTelemetry'][0]['Status']+" : "+vpn['VgwTelemetry'][1]['Status'])
                    #slack_client.api_call( "chat.postMessage", channel=schannel, text=  "[ERROR] "+vpn['VpnConnectionId']+" is "+vpn['State']+"; tunnels: "+vpn['VgwTelemetry'][0]['Status']+" : "+vpn['VgwTelemetry'][1]['Status'])
                    continue
                else:
                    # success
                    print( "[SUCCESS] "+vpn['VpnConnectionId']+" is "+vpn['State']+"; tunnels: "+vpn['VgwTelemetry'][0]['Status']+" : "+vpn['VgwTelemetry'][1]['Status'])
                    # do not send slack output for success - except for testing
                    #slack_client.api_call( "chat.postMessage", channel=schannel, text=  "[SUCCESS] "+vpn['VpnConnectionId']+" is "+vpn['State']+"; tunnels: "+vpn['VgwTelemetry'][0]['Status']+" : "+vpn['VgwTelemetry'][1]['Status'])

       '''
    except Exception as e:
        print("Exception: "+ str(e))
    
    
