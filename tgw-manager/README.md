# usctransitgateway::management-scripts component
Management scripts for the USC transit gateway project.  Customer information is stored in dynamoDB table.  Create scripts for:
- transit gateway: resource share the tgw to a single account 
- transit gateway: resource share the tgw to a multiple accounts.  Compare attachments in dynamoDB vs attachments on the tgw.  Send resource shares to missing VPCs
- transit gateway: report attachments in dynamoDB vs attachments on the tgw
- TBD


## DynamoDB scan - test script
This test script runs on EC2 instance.  Make sure python2 and/or python3 are installed.  
This code dumps all the items in the DynamoDB table

To run on command-line: 
python3 scan_dynamodb_table.py


## Transit Gateway show attachment - test script
This test script runs on EC2 instance.  Make sure python2 and/or python3 are installed.  
This code dumps all the items in the DynamoDB table

To run on command-line: 
python3 show_tgw_attachments.py


## Transit Gateway Manager - (early development) production application
This test script runs on EC2 instance.  Make sure python2 and/or python3 are installed.  
This application will access dynamodb table and run commands on the EC2 Transit Gateway

To run on command-line: 
python3 usc-manage-tgw.py

********************** TGW MANAGER **********************

Checking that this EC2 meets requirements for TGW Manager ...

- EC2 service supports TGW model...passed

- IAM role for API permissions attached to EC2...passed

All requirements have passed!!
********************** TGW MANAGER **********************

What would you like to do? Choose option A - I:
--------------------------------------------------------
A) Check Transit Gateway from DynamoDB
B) Check Transit Gateway from EC2
C) RAM: re-share TGWs (TBD)

H) Help
X) Exit
--------------------------------------------------------
> A

(1) Transit Gateway, (1) VPCs, (1) VPNs
Transit Gateway (tgw-07c16ca582c6fbee9) CIDR (10.254.0.0/16)

    VPC (vpc-0f1ce0dca956a2c2d) CIDR (10.254.4.0/24)

    VPN (vpn-01dd07c2c43662ff0) CIDR (207.151.53.254/32)

What would you like to do? Choose option A - I:
--------------------------------------------------------
A) Check Transit Gateway from DynamoDB
B) Check Transit Gateway from EC2
C) RAM: re-share TGWs (TBD)

H) Help
X) Exit
--------------------------------------------------------
> B

(1) Transit Gateway, (3) VPCs, (1) VPNs
Transit Gateway (tgw-07c16ca582c6fbee9)

    VPC (vpc-0ffddd04431937a08)
    VPC (vpc-00e3e42349e3b8ca8)
    VPC (vpc-0f1ce0dca956a2c2d)

    VPN (vpn-01dd07c2c43662ff0)






## TBD


## Comments
