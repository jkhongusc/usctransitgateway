import boto3
import json
import sys
from region import region

class TgwEc2:


    cache_file = 'cache_ec2.json'

    def __init__(self):
        #self.name = name
        self.ec2 = boto3.client('ec2')
        self.cache = self.load_from_ec2()
        #print (self.cache)
        #sys.exit()

    def load_from_ec2(self):
        cache = self.ec2.describe_transit_gateway_attachments()
        #Filters=[{'Name':'transit-gateway-id','Values':['tgw-07c16ca582c6fbee9']}]

        # remove any keys that cannot be serialized or convert to serializable type
        for item in cache['TransitGatewayAttachments']:
            item.pop('CreationTime',None)
        self.cache = cache
        #print (self.cache)
        #sys.exit()
        try:
            with open(self.cache_file,'w') as f:
                json.dump(self.cache['TransitGatewayAttachments'], f)
            f.close()
        except Exception as e:
            # ignore write errors
            print ("file error: "+str(e))
            pass
        return self.cache['TransitGatewayAttachments']

    def load_from_file(self):
        try:
            with open(self.cache_file,'r') as f:
                self.cache = json.load(f)
            f.close()
        except Exception as e:
            # if file error, load from ec2 
            # store results in cache
            self.cache = self.load_from_ec2()
        return self.cache

    def get_transit_gateway(self):
        #print (self.cache)
        tgw_list = []
        for item in self.cache:
            tgw_item = { 'TransitGatewayId': None, 'Cidr': None }
            if any(d['TransitGatewayId'] != tgw_item['TransitGatewayId'] for d in tgw_list):
                continue
            tgw_item['TransitGatewayId'] = item['TransitGatewayId']
            #tgw_item['Cidr'] = item['Cidr']
            tgw_list.append(tgw_item)
        return tgw_list
            
    def get_vpc(self):
        #print (self.cache)
        vpc_list = []
        for item in self.cache:
            vpc_item = { 'ResourceId': None, 'Cidr': None }
            if item['ResourceType'] != 'vpc':
                continue
            vpc_item['ResourceId'] = item['ResourceId']
            #vpc_item['Cidr'] = item['Cidr']
            #vpc_list.append(vpc_item)
            vpc_list.append(item)
        return vpc_list

    def get_vpn(self):
        #print (self.cache)
        vpn_list = []
        for item in self.cache:
            vpn_item = { 'ResourceId': None, 'Cidr': None }
            if item['ResourceType'] != 'vpn':
                continue
            vpn_item['ResourceId'] = item['ResourceId']
            #vpn_item['Cidr'] = item['Cidr']
            #vpn_list.append(vpn_item)
            vpn_list.append(item)
        return vpn_list
            
        
        
        






