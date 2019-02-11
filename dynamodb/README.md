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


## Attributes - planning
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


## Attributes - implementation
Attributes Names, Type, and Description:
- Account [String]: AWS account number
- Cidr [String]: CIDR
- TransitGatewayId [String]: Transit Gateway ID that resource is attached/associated
- Department [String]: USC department name
- OwnerEmail [String]: Business owner's email address
- TechEmail [String]: Business technical contact email address
- ResourceType [String]: type of resource.  Should be one of: 
  - hub - signifies that this entry is for the transit gateway.  There should only be one hub, but this design allows the possibility of multiple hubs (transit gateways per region)
  - vpc - signifies that a VPC is associated with the transit gateway
  - vpn - signifies that a VPN is associated with the transit gateway
- ResourceId [String]: AWS ID of ResourceType
- Configuration [String]: any extra configuration information required.  Might be required for hub
- Description [String]: any extra information to describe entry
-  [String]:


## Comments
- For DynamoDB CFT, only attributes used for keys or indexing are defined in schema

