# usctransitgateway::DynamoDB component
Information regarding the configuration data stored for the USC transit gateway project.  

Data could have been stored in a SQL or no-SQL database.  DynamoDB was selected for this use-case which would be a small table of up to 500 items.


## Design
Dynamo DB design:
- partition key - Transit Gateway
- sort key - CIDR
- global secondary index - none
- local secondary index - none
- attributes (see below)

## Attributes
Attributes:
- Hub information:
  - Transit gateway - 
  - configuration - transit gateway configuration details in json
- Customer information:
  - USC Department name
  - Owner - email
  - Tech contact - email address
  - security level: 1L,2L,3L
  - environment: dev,test,stage,production,non-production, etc
- AWS information:
  - account
  - CIDR
  - CFT
  - VPC
  - Transit gateway id - use the same "Transit gateway" field from the hub
- miscellaneous:
  - start date
  - end date
  - comments
  - description

## Comments
