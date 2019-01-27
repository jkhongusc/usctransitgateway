# usctransitgateway-uswest2::DynamoDB component
Information regarding the configuration data stored for the USC transit gateway project.  

Data could have been stored in a SQL or no-SQL database.  DynamoDB was selected for this use-case which would be a small table of up to 500 items.


## Design
Dynamo DB design:
- partition key - AWS account
- sort key - CIDR
- global secondary index - none
- local secondary index - none
- attributes (see below)

## Attributes
Attributes:
- Hub information:
  - Transit gateway - probably not required.  
  - Route table(s) - probably not required
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
  - Transit gateway id 
  - transit gateway route table association
  - transit gateway route table propagation
- miscellaneous:
  - start date
  - end date
  - comments
  - description
  - data

## Comments
