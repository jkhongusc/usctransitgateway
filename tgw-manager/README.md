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




## TBD


## Comments
