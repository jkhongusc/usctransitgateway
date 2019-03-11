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

import os
import boto3

from dynamodb import TgwDynamoDb
from ec2 import TgwEc2
from ram import TgwRam


#print('Loading function')
#cw = boto3.client('cloudwatch')



def lambda_handler(event, context):
    # check to make sure all required parameters are defined
    #if 'SLACKTOKEN' not in os.environ:
    #    raise Exception('SLACKTOKEN environment variable not set')
    if 'SLACKNAME' not in os.environ:
        raise Exception('SLACKNAME environment variable not set')
    if 'SLACKCHANNEL' not in os.environ:
        raise Exception('SLACKCHANNEL environment variable not set')

    if 'REGION' not in event:
        raise Exception('REGION event variable not set')
    if 'TRANSITGATEWAY' not in event:
        raise Exception('TRANSITGATEWAY event variable not set')
    if 'RAMSHARENAME' not in event:
        raise Exception('RAMSHARENAME event variable not set')

    #stoken=os.environ['SLACKTOKEN']
    sname=os.environ['SLACKNAME']
    schannel=os.environ['SLACKCHANNEL']
    region=event['REGION']
    tgws=event['TRANSITGATEWAY']
    ramsharenames=event['RAMSHARENAME']

    #slack_client = SlackClient(stoken)
    #slack_client.api_call( "chat.postMessage", channel=schannel, text="test from EC2")
    
    try:

        print ("starting")
        myram = TgwRam(region)
        ramprincipals = myram.get_principals()
        print("[RAM] Transit Gateway, (%d) Principals" % (len(ramprincipals)) )
        #print (ramprincipals)
        for ramprincipal in ramprincipals:
            print("    AWS (%s)" % (ramprincipal['id']) )

        myec2 = TgwEc2(region)
        vpcattachments = myec2.get_transit_gateway_vpc_attachments()
        print("[EC2] Transit Gateway Attachments (%d) " % (len(vpcattachments)) )
        for vpcattachment in vpcattachments:
            print("    AWS (%s) VPC (%s)" % (vpcattachment['VpcOwnerId'],vpcattachment['VpcId']) )

        mydynamo = TgwDynamoDb(region)
        tgwlist = mydynamo.get_transit_gateway() 
        vpclist = mydynamo.get_vpc() 
        vpnlist = mydynamo.get_vpn() 
        print("[DynamoDb] (%d) Transit Gateway, (%d) VPCs, (%d) VPNs" % (len(tgwlist),len(vpclist),len(vpnlist)) )
        for tgwitem in tgwlist:
            print("Transit Gateway (%s) CIDR (%s) AWS (%s) VPC (%s)" % (tgwitem['TransitGatewayId'],tgwitem['Cidr'],tgwitem['Account'],tgwitem['ResourceId']) )
        #print (vpclist)
        for vpcitem in vpclist:
            print("    VPC (%s) CIDR (%s) AWS (%s)" % (vpcitem['ResourceId'],vpcitem['Cidr'],vpcitem['Account']) )
        #print (vpnlist)
        for vpnitem in vpnlist:
            print("    VPN (%s) CIDR (%s) AWS (%s)" % (vpnitem['ResourceId'],vpnitem['Cidr'],vpnitem['Account']) )
        

        # Add comparisons/notification/alerts here


        # iterate through DynamoDB VPC list
        # check if VPC is in Transit Gateway Attachment list, if not create alert
        # for errors: account admin has to manually check or attach
        print ("\nNotifications")
        print ("Check #1: DynamoDB and Transit Gateway Attachments")
        for vpcitem in vpclist:
            if not any (d['VpcId'] == vpcitem['ResourceId'] for d in vpcattachments):
                print("    [ERROR] VPC (%s) CIDR (%s) AWS (%s) is not found in TGW Attachment list" % (vpcitem['ResourceId'],vpcitem['Cidr'],vpcitem['Account']) )
            else:
                print("    VPC (%s) CIDR (%s) AWS (%s) is found in TGW Attachment list" % (vpcitem['ResourceId'],vpcitem['Cidr'],vpcitem['Account']) )


        # iterate through Transit Gateway Attachment list
        # check if VPC is in DynamoDB VPC list, if not create alert
        # for errors: account admin has to manually check
        print ("Check #2: Transit Gateway Attachments and DynamoDb")
        for vpcattachment in vpcattachments:
            if not any (d['ResourceId'] == vpcattachment['VpcId'] for d in vpclist):
                print("    [ERROR] VPC (%s) AWS (%s) is not found in DynamoDb list" % (vpcattachment['VpcId'],vpcattachment['VpcOwnerId']) )
            else:
                print("    VPC (%s) AWS (%s) is found in DynamoDb list" % (vpcattachment['VpcId'],vpcattachment['VpcOwnerId']) )


        # iterate through DynamoDB VPC list, ignore VPCs from master account
        # check if VPC is in RAM principal list, if not create alert
	# for errors: automatically create new resource share with principal (should check invitations first)
        print ("Check #3: DynamoDB and RAM")
        for vpcitem in vpclist:
            if (vpcitem['Account'] == tgwitem['Account']):
                print("    VPC (%s) CIDR (%s) AWS (%s) is found in master account" % (vpcitem['ResourceId'],vpcitem['Cidr'],vpcitem['Account']) )
                continue
            #if not any (d['Account'] == vpcitem['Account'] for d in vpclist):
            if not any (d['id'] == vpcitem['Account'] for d in ramprincipals):
                print("    [ERROR] VPC (%s) CIDR (%s) AWS (%s) is not found in RAM list" % (vpcitem['ResourceId'],vpcitem['Cidr'],vpcitem['Account']) )
                print ("        sending RAM resource share to: " + vpcitem['Account'])
                #print ("%s arn:aws:ec2:%s:%s:transit-gateway/%s %s," %( ramsharenames[0], region, tgwitem['Account'], tgwitem['TransitGatewayId'], vpcitem['Account'] ))
	        # TBD - for errors: automatically create new resource share with principal
                response = myram.create_resource_share( ramsharenames[0],  ['arn:aws:ec2:'+region+':'+tgwitem['Account']+':transit-gateway/'+tgwitem['TransitGatewayId'] ],[ vpcitem['Account']])
                #print (response)

            else:
                print("    VPC (%s) CIDR (%s) AWS (%s) is found in RAM list" % (vpcitem['ResourceId'],vpcitem['Cidr'],vpcitem['Account']) )







        '''
        # iterate through RAM list which is a list of VPCs
        # check if RAM VPC is in DynamoDB list, if not create alert
        print ("Check #3: RAM list")
        for ramprincipal in ramprincipals:
            if not any (d['Account'] == ramprincipal['id'] for d in vpclist):
                print("    [ERROR] AWS (%s) is not found in DynamoDB list" % (ramprincipal['id']) )
            else:
                print("    AWS (%s) is found in DynamoDB list" % (ramprincipal['id']) )
        '''



        
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
    
    
