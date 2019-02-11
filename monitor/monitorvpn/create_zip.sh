#!/bin/sh

# should be in the base directory
cd lib/python3.7/site-packages

zip -r9 ../../../monitorvpn.zip *

cd ../../..

zip -g monitorvpn.zip main.py

