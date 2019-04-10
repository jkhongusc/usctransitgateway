import boto3
import json
import sys

class TgwRam:


    def __init__(self,region):
        #self.name = name
        self.region = region
        self.client = boto3.client('ram')
        
        #print (self.cache)
        #sys.exit()

    def list_principals (self):
        response = self.client.list_principals(resourceOwner='SELF')
        return response['principals']

    def get_principals (self):
        return self.list_principals()


    def get_transit_gateway(self):
        #print (self.cache)
        tgw_list = []
        for item in self.cache:
            # should we only send specific keys or the whole dict obj - code for both
            tgw_item = { 'TransitGatewayId': None, 'Cidr': None }
            if item['ResourceType'] != 'hub':
                continue
            tgw_item['TransitGatewayId'] = item['TransitGatewayId']
            tgw_item['Cidr'] = item['Cidr']
            #tgw_list.append(tgw_item)
            tgw_list.append(item)
        #print (tgw_list)
        return tgw_list
            
    def get_vpc(self):
        #print (self.cache)
        vpc_list = []
        for item in self.cache:
            # should we only send specific keys or the whole dict obj - code for both
            vpc_item = { 'ResourceId': None, 'Cidr': None }
            if item['ResourceType'] != 'vpc':
                continue
            vpc_item['ResourceId'] = item['ResourceId']
            vpc_item['Cidr'] = item['Cidr']
            #vpc_list.append(vpc_item)
            vpc_list.append(item)
        return vpc_list

    def get_vpn(self):
        #print (self.cache)
        vpn_list = []
        for item in self.cache:
            # should we only send specific keys or the whole dict obj - code for both
            vpn_item = { 'ResourceId': None, 'Cidr': None }
            if item['ResourceType'] != 'vpn':
                continue
            vpn_item['ResourceId'] = item['ResourceId']
            vpn_item['Cidr'] = item['Cidr']
            #vpn_list.append(vpn_item)
            vpn_list.append(item)
        return vpn_list

    def get_resource_share_associations(self,associationType,resourceShareArns=list(),resourceArn=None,principal=None,associationStatus=list()):
        if len(resourceShareArns) == 0 and len(associationStatus) > 0:
            #response = self.client.get_resource_share_associations(associationType=associationType,resourceArn=resourceArn,principal=principal,associationStatus=associationStatus)
            response = self.client.get_resource_share_associations(associationType=associationType,principal=principal,associationStatus=associationStatus)
        elif len(resourceShareArns) > 0 and principal == None:
            response = self.client.get_resource_share_associations(associationType=associationType,resourceShareArns=resourceShareArns)
        else:
            response = self.client.get_resource_share_associations(associationType=associationType,resourceShareArns=resourceShareArns,principal=principal)
        return response['resourceShareAssociations']

    def create_resource_share(self,name,arns,principals):
        response = self.client.create_resource_share(name=name,resourceArns=arns,principals=principals,allowExternalPrincipals=True)
        return response

    def associate_resource_share(self,resourceShareArns,resourceArns,principals):
        response = self.client.get_resource_share_associations(associationType=associationType,resourceShareArns=resourceShareArns)
        return response



        
