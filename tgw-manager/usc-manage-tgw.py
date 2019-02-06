#! /usr/bin/python2.7

import subprocess
import os
import sys
import re
import time
import threading


# If there is a ImportError exception, then prompt user to install proper modules for this program
def import_modules():

    os.system('clear')
    print("********************** TGW MANAGER **********************\n")
    # Create a nifty little spinning cursor
    def spin_cursor():
        while True:
            for cursor in '|/-\\':
                sys.stdout.write(cursor)
                sys.stdout.flush()
                time.sleep(0.1) # adjust this to change the speed
                sys.stdout.write('\b')
                if done:
                    return
    spin_thread = threading.Thread(target=spin_cursor)

    try:
        import boto3
        import prettytable
    except:
        print("\nInstalling necessary python modules...")
        done = False
        spin_thread.start()
        FNULL = open(os.devnull,'w')
        subprocess.call(['sudo','pip','install','boto3'], stdout=FNULL, stderr=subprocess.STDOUT)
        subprocess.call(['sudo','pip','install','prettytable'], stdout=FNULL, stderr=subprocess.STDOUT)
        subprocess.call(['sudo','pip','install','botocore==1.10.82'], stdout=FNULL, stderr=subprocess.STDOUT)
        subprocess.call(['sudo','pip','install','--upgrade','awscli'], stdout=FNULL, stderr=subprocess.STDOUT)

        done = True
        spin_thread.join()
        pass
import_modules()

def check_model():
    import boto3
    from botocore.exceptions import NoCredentialsError
    ec2 = boto3.client('ec2', region_name = 'us-west-2')

    print("\n\nChecking that this EC2 meets requirements for TGW Manager ...")
    # See if the TGW model has been added to the EC2 service
    try:
        ec2.describe_transit_gateways()
        print("\n- EC2 service supports TGW model...passed")
        print("\n- IAM role for API permissions attached to EC2...passed")

    except AttributeError:
        print("\n'ec2' service supports TGW model...failed\n"
             "Be sure to add the 'service-2.json' model to the 'ec2' service\n"
             "to meet this requirement.\n")
        sys.exit()
    
    except NoCredentialsError:
        print("\nIAM role for API permissions attached to EC2...failed\n"
              "You should have an IAM role attached to this that allows the\n"
              "following permissions:\n\n"
              "ec2:CreateTransitGateway\n"
              "ec2:CreateTransitGatewayVpcAttachment\n"
              "ec2:CreateRoute\n"
              "ec2:DescribeTransitGateways\n"
              "ec2:DescribeSubnets\n"
              "ec2:DescribeVpcs\n"
              "ec2:DescribeAvailabilityZones\n"
              "ec2:DescribeRouteTables\n"
              "ec2:DescribeCustomerGateways\n"
              "ec2:DescribeVpnConnections\n"
              "ec2:DescribeVpnGateways\n"
              "ec2:DescribeTransitGatewayVpcAttachments\n"
              "ec2:DeleteTransitGatewayVpcAttachment\n"
              "ec2:DeleteRoute\n")
             
        sys.exit()
    
    print("\nAll requirements have passed!!\n")

check_model()


sys.path.insert(0,'dependencies/')

# see if region file is already set or not
try:
	f = open('dependencies/region.py', 'r')
except:
    os.system('clear')
    print("********************** TGW MANAGER **********************\n")
    def get_region():
        region = input("What region do you want to run the TGW Migrator in?\n"
                           "Note: You will only be able to migrate VPCs to this\n"
                           "tool that are in the region you specify below.\n"
                        "---------------------------------------------------\n"
                        "us-west-2> ") or "us-west-2"

        region = region.replace(' ','')
        m = re.match('^[a-z]{2}\-[a-z]{4,9}\-\d$', region)
        if m:
            with open('dependencies/region.py', 'w+') as f:
                f.write("region=\'%s\'" % region)
        else:
            print("\nYou must specify a valid AWS region. Example: us-west-2\n")
            get_region()

    get_region()
from tgwmanager import tgwmanager 

tgwmanager()
