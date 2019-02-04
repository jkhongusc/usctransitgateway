# usctransitgateway::CloudFormation 
CloudFormation templates for the USC transit gateway project
- hub  
  - [cloudtrail.yaml](hub/cloudtrail.yaml)- CFT that creates and configures the minimum AWS resources
  - [transiteyateway.yaml](hub/transitgateway.yaml) - CFT that creates the transit gateway.  Note that not all tgw configurations are supported in CFT; so these configurations will need to be done outside of the CFT either manually or programmatically.
- spoke
  - [cidr24_3az.yaml](spoke/cidr24_3az.yaml) - 
  - [cidr25-2az.yaml](spoke/cidr25_2az.yaml) - CFT that creates a /25 VPC with two /26 subnets in separate AZs
