# usctransitgateway::CloudFormation 
CloudFormation templates for the USC transit gateway project
- hub  
  - [cloudtrail.yaml](hub/cloudtrail.yaml)- CFT that creates and configures the minimum AWS resources
  - [transitgateway.yaml](hub/transitgateway.yaml) - CFT that creates the transit gateway.  Note that not all tgw configurations are supported in CFT; so these configurations will need to be done outside of the CFT either manually or programmatically.
  - [DynamicDNS.yaml](hub/DynamicDNS.yaml)- CFT that creates private hosted zone, EC2 CloudWatch rule, and lambda function that execute Python code in S3 bucket
- spoke
  - [cidr24_3az.yaml](spoke/cidr24_3az.yaml) - CFT that creates /24 VPC with three /26 subnets in separate AZs
  - [cidr_1az.yaml](spoke/cidr_2az.yaml) - CFT that creates any size VPC with one subnets
  - [cidr_2az.yaml](spoke/cidr_2az.yaml) - CFT that creates any size VPC with two subnets in separate AZs


test
