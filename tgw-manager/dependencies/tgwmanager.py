#! /usr/bin/python2.7
import boto3
import os
import sys
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
from region import region

from dynamodb import TgwDynamoDb
from ec2 import TgwEc2
#from create_tgw import create_tgw
#from attach_spoke_vpcs import attach_spoke_vpcs
#from list_attachments import list_attachments
#from add_routes import add_routes
#from detach_vpcs import detach_vpcs
#from create_ram import create_ram
#from delete_routes import delete_routes
#from update_accounts import update_accounts

dynamodb = boto3.resource('dynamodb', region_name = region)
#table = dynamodb.Table('TgwMigrationTable')
table = dynamodb.Table('dynamodb-tgw-table')
dynamodbcache_file = 'dynamodbcache.json'

def loadtable():
    # load all data from DynamoDB table
    # cache items in file
    response = table.scan ( )
    #print (response)
    #sys.exit()
    with open(dynamodbcache_file,'w') as f:
        json.dump(response['Items'], f)
    return response['Items']



def tgwmanager():
    mydynamo = TgwDynamoDb()
    myec2 = TgwEc2()
    #sys.exit()
    #myec2 = Tgwec2()

    def check_for_tgw():
        mydata = loadtable()
        #print (mydata)
        print("\nFound (%s) transit gateway registered for region %s" % (mydata,region) )
        sys.exit()

        dynamodbcache_file = 'dynamodbcache.json'
        response = table.scan ( )
        with open(dynamodbcache_file,'w') as f:
            json.dump(response['Items'], f)
#with open("data_file.json", "r") as rf:
#data = json.load(rf)
        print (response)
        sys.exit()
        # should we print out other information about the tgw like CIDR range?
        print("\nFound (%s) transit gateway registered for region %s" % (response['Count'],region) )
	# Should only find one tgw.  Should we support multiple?
        print("\nTransit Gateway: (%s) " % response['Items'][0]['TransitGateway'])

        try:
#            if response['Item']['TgwId']:
            if response['Items'][0]['TransitGateway']:
                # TGW exists. Store its Id
#                tgw_id = response['Item']['TgwId']
                tgw_id = response['Items'][0]['TransitGateway']
                os.system('clear')
                print("\nA TGW (%s) has been registered in this tool" % tgw_id)
                return tgw_id

        except KeyError:
            # Create TGW and store its Id
            os.system('clear')
            print("\nThis tool does not currently have a TGW id registered with it...")
#            tgw_id = create_tgw(table)
            return tgw_id

    os.system('clear')
    print("********************** TGW MANAGER **********************\n")
    def ask_question():
        user_response = input("\nWhat would you like to do? Choose option A - I:\n"
                                    "--------------------------------------------------------\n"
                                    "A) Check Transit Gateway from DynamoDB\n"
                                    "B) Check Transit Gateway from EC2\n"
                                    "C) Check Transit Gateway \n"
#                                    "B) Share registered TGW with other AWS accounts\n"
#                                    "C) Attach VPCs to registered TGW\n"
#                                    "D) Enable routing between attached VPCs\n"
#                                    "E) Disable routing between attached VPCs\n"
#                                    "F) List existing VPC attachments\n"
#                                    "G) Detach VPCs and deregister TGW\n"
#                                    "H) Add or delete secondary AWS accounts\n"
                                    "X) Exit\n"
                                    "--------------------------------------------------------\n"
                                    "> ")                   

        if user_response.lower() == 'a':
            # User wants to create or add TGW
            tgwlist = mydynamo.get_transit_gateway() 
            vpclist = mydynamo.get_vpc() 
            vpnlist = mydynamo.get_vpn() 
            print ("\n")
            print("(%d) Transit Gateway, (%d) VPCs, (%d) VPNs" % (len(tgwlist),len(vpclist),len(vpnlist)) )
            for tgwitem in tgwlist:
                print("Transit Gateway (%s) CIDR (%s)" % (tgwitem['TransitGateway'],tgwitem['Cidr']) )
            print ("\n")
            for vpcitem in vpclist:
                print("    VPC (%s) CIDR (%s)" % (vpcitem['ResourceId'],vpcitem['Cidr']) )
            print ("\n")
            for vpnitem in vpnlist:
                print("    VPN (%s) CIDR (%s)" % (vpnitem['ResourceId'],vpnitem['Cidr']) )
            ask_question()

        if user_response.lower() == 'b':
            # User wants to share TGW with other accounts
            tgwlist = myec2.get_transit_gateway() 
            vpclist = myec2.get_vpc() 
            vpnlist = myec2.get_vpn() 
            print ("\n")
            print("(%d) Transit Gateway, (%d) VPCs, (%d) VPNs" % (len(tgwlist),len(vpclist),len(vpnlist)) )
            for tgwitem in tgwlist:
                print("Transit Gateway (%s)" % (tgwitem['TransitGatewayId']) )
            print ("\n")
            for vpcitem in vpclist:
                print("    VPC (%s) " % (vpcitem['ResourceId']) )
            print ("\n")
            for vpnitem in vpnlist:
                print("    VPN (%s) " % (vpnitem['ResourceId']) )
            #create_ram(table,tgw_id)
            ask_question()

        elif user_response.lower() == 'c':
            # User wants to attach VPCs. First check TGW existence
            tgw_id = check_for_tgw()
            attach_spoke_vpcs(table,tgw_id)

        elif user_response.lower() == 'd':
            # User wants to enable routing between VPCs
            tgw_id = check_for_tgw() 
            add_routes(table,tgw_id)
        
        elif user_response.lower() == 'e':
            # User wants to disable routing from VPCs and detach them from TGW
            tgw_id = check_for_tgw() 
            delete_routes(table,tgw_id)

        elif user_response.lower() == 'f':
            # List out the VPC attachments in DB
            tgw_id = check_for_tgw() 
            list_attachments(table)
            ask_question()
        
        elif user_response.lower() == 'g':
            # Deregister and delete TGW
            tgw_id = check_for_tgw() 
            detach_vpcs(table,tgw_id)
        
        elif user_response.lower() == 'h':
            # Update secondary accounts
            update_accounts()
        
        elif user_response.lower() == 'q' or user_response.lower() == 'x':
            # Exit to CLI
            os.system('clear')
            print("\nBye!!\n")
            sys.exit()
        
        else:
            print("\nPlease choose a valid option")
            ask_question()

        print("\nDone !!!\n")
        ask_question()
    ask_question()
