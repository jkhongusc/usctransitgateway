import boto3
import json
import sys

class TgwEc2:


    #def __init__(self,region=None,transitgateway=None):
    def __init__(self,region):
        '''
        #self.name = name
        if region is None:
            self.region = None
        else:
            self.region = region
        if transitgateway is None:
            self.transitgateway = None
        else:
            self.transitgateway = transitgateway
        '''
        self.region = region
        self.client = boto3.client('ec2',region)


    def get_transit_gateway_attachments(self):
        #print (self.cache)
        response = self.client.describe_transit_gateway_attachments(
            #Filters=[{'Name':'transit-gateway-id','Values':[self.transitgateway]}]
        )
        #print(response)
        return response['TransitGatewayAttachments']

            
    def get_transit_gateway_vpc_attachments(self):
        #print (self.cache)
        response = self.client.describe_transit_gateway_vpc_attachments(
            #Filters=[{'Name':'transit-gateway-id','Values':[self.transitgateway]}]
        )
        #print(response)
        return response['TransitGatewayVpcAttachments']
            
        
