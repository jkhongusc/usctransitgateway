import boto3
import json
import sys
from region import region

class TgwDynamoDb:


    cache_file = 'cache_dynamodb.json'
    table_name = 'dynamodb-tgw-table'

    def __init__(self):
        #self.name = name
        self.dynamo = boto3.resource('dynamodb', region_name = region)
        self.table = self.dynamo.Table(self.table_name)
        self.cache = self.load_from_dynamodb()
        #print (self.cache)
        #sys.exit()

    def load_from_dynamodb(self):
        response = self.table.scan ( )
        #print (response)
        #sys.exit()
        try:
            with open(self.cache_file,'w') as f:
                json.dump(response['Items'], f)
            f.close()
        except Exception as e:
            # ignore write errors
            #print ("file error: "+str(e))
            pass
        return response['Items']

    def load_from_file(self):
        try:
            with open(self.cache_file,'r') as f:
                self.cache = json.load(f)
            f.close()
        except Exception as e:
            # if file error, load from dynamodb
            # store results in cache
            self.cache = self.load_from_dynamodb()
        return self.cache

    def get_transit_gateway(self):
        #print (self.cache)
        tgw_list = []
        for item in self.cache:
            # should we only send specific keys or the whole dict obj - code for both
            tgw_item = { 'TransitGateway': None, 'Cidr': None }
            if item['ResourceType'] != 'hub':
                continue
            tgw_item['TransitGateway'] = item['TransitGateway']
            tgw_item['Cidr'] = item['Cidr']
            #tgw_list.append(tgw_item)
            tgw_list.append(item)
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
            
        
        
        






