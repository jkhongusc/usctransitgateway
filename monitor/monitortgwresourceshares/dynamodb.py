import boto3
import json
import sys

class TgwDynamoDb:

    table_name = 'dynamodb-tgw-table'

    def __init__(self,region):
        #self.name = name
        self.region = region
        self.dynamo = boto3.resource('dynamodb', region_name = self.region)
        self.table = self.dynamo.Table(self.table_name)
        self.cache = self.load_from_dynamodb()
        #print (self.cache)
        #sys.exit()

    def load_from_dynamodb(self):
        response = self.table.scan ()
        return response['Items']


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
            if item['ResourceType'] != 'vpc' and item['ResourceType'] != 'hub':
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

    def get_resource_shares(self):
        #print (self.cache)
        rs_list = []
        for item in self.cache:
            # should we only send specific keys or the whole dict obj - code for both
            rs_item = { 'resourceShareArn': None }
            if item['ResourceType'] != 'hub':
                continue
            config = json.loads(item['Configuration'])
            #rs_item['resourceShareArn'] = rs_item['Configuration']
            rs_item['resourceShareArn'] = config['resourceShareArn']
            #print (rs_item['resourceShareArn'])
            rs_list.append(rs_item)
        return rs_list



            
