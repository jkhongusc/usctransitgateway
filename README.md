# usctransitgateway-uswest2
USC transit gateway project


## github access
Ask owner for read/write access.  

To clone:
git clone https://<github user>:<github token>@github.com/jkhongusc/usctransitgateway .


## Development environment
I recommend creating a development environment on a standard EC2 Linux instance (micro is usually enough):
- Create EC2 instance 
  - Use latest Amazon Linux AMI
  - select micro instance
  - Make sure EC2 is launched in the correct VPC
  - configure IAM role to apply to instance (this step can be modified post launch)
  - apply security group (SG can be modified post launch)
  - apply EC2 key pair
- ssh to instance and install any necessary packages:
  - sudo yum install git
  - python3
