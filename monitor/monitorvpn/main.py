import boto3
#import time
#import re
#import sys
import os
from slackclient import SlackClient

def lambda_handler(event, context):

    # check to make sure all required parameters are defined
    if 'SLACKTOKEN' not in os.environ:
        raise Exception('SLACKTOKEN environment variable not set')
    if 'SLACKNAME' not in os.environ:
        raise Exception('SLACKNAME environment variable not set')
    if 'SLACKCHANNEL' not in os.environ:
        raise Exception('SLACKCHANNEL environment variable not set')

    if 'REGION' not in event:
        raise Exception('REGION event variable not set')
    if 'VPN' not in event:
        raise Exception('VPN event variable not set')

    stoken=os.environ['SLACKTOKEN']
    sname=os.environ['SLACKNAME']
    schannel=os.environ['SLACKCHANNEL']
    region=event['REGION']
    monitor_vpns=event['VPN']

    slack_client = SlackClient(stoken)
    #slack_client.api_call( "chat.postMessage", channel=schannel, text="test from EC2")

    try:
        ec2 = boto3.client('ec2',region_name=region)
        response = ec2.describe_vpn_connections()
        vpns = response['VpnConnections']

        for monitor_vpn in monitor_vpns:
#            if not any(vpn['VpnConnectionId'] == monitor_vpn for vpn in vpns)
            if not any(vpn['VpnConnectionId'] == monitor_vpn for vpn in vpns):
                print( "[ERROR] "+monitor_vpn+" not found")
                slack_client.api_call( "chat.postMessage", channel=schannel, text="[ERROR] "+monitor_vpn+" not found")
                continue
            for vpn in vpns:
                if (vpn['VpnConnectionId'] != monitor_vpn):
                    print ("skipping: "+vpn['VpnConnectionId'])
                    continue
                if (vpn['State'] != 'available' or vpn['VgwTelemetry'][0]['Status'] != 'UP' or
                    vpn['VgwTelemetry'][1]['Status'] != 'UP'): 
                    # error
                    print( "[ERROR] "+vpn['VpnConnectionId']+" is "+vpn['State']+"; tunnels: "+vpn['VgwTelemetry'][0]['Status']+" : "+vpn['VgwTelemetry'][1]['Status'])
                    slack_client.api_call( "chat.postMessage", channel=schannel, text=  "[ERROR] "+vpn['VpnConnectionId']+" is "+vpn['State']+"; tunnels: "+vpn['VgwTelemetry'][0]['Status']+" : "+vpn['VgwTelemetry'][1]['Status'])
                    continue
                else:
                    # success
                    print( "[SUCCESS] "+vpn['VpnConnectionId']+" is "+vpn['State']+"; tunnels: "+vpn['VgwTelemetry'][0]['Status']+" : "+vpn['VgwTelemetry'][1]['Status'])
                    # do not send slack output for success - except for testing
                    #slack_client.api_call( "chat.postMessage", channel=schannel, text=  "[SUCCESS] "+vpn['VpnConnectionId']+" is "+vpn['State']+"; tunnels: "+vpn['VgwTelemetry'][0]['Status']+" : "+vpn['VgwTelemetry'][1]['Status'])

    except Exception as e:
        print("Exception: "+ str(e))




