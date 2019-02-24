#!/bin/sh

# should be in the base directory
cd lib/python3.7/site-packages

zip -r9 ../../../monitortgwresourceshares.zip *

cd ../../..

zip -g monitortgwresourceshares.zip main.py

