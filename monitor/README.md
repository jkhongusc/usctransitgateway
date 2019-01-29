# usctransitgateway::monitor component
Monitoring components for the USC transit gateway project
- VPN 
- TBD


## VPN monitoring - test script
This test script runs on EC2 instance.  Make sure python2 and/or python3 are installed.  
This code can be used as a basis to build a lambda VPN monitoring function.  

To run on command-line: 
python3 check_vpn_test.py

Output: 
[ec2-user@ip-172-31-16-158 monitor]$ python3 check_vpn_test.py
vpn-01dd07c2c43662ff0
  available
    UP
    UP

Shows all the VPN connections for the account.  For each VPN connection: vpn id, VPN state, tunnel states


## TBD


## Comments
