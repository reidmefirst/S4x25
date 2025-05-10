#!/usr/bin/python3
###
### rulechecker.py
### checks your suricata ruleset to make sure you aren't making a common mistake:
### forgetting to including a flow direction in rules that use tcp or udp ports
### above 1024.
###
### this tool accompanies the S4x25 talk titled
### "Your IDS rules for ICS Stink (and how to fix them)"
### for noncommercial use only
###
### you will need the 'idstools' package
### it is available from github at https://github.com/jasonish/py-idstools .
### the readme on this project has install instructions:
### pip install https://github.com/jasonish/py-idstools/archive/master.zip

from idstools import rule
import argparse

argparser = argparse.ArgumentParser(description="suricata rule verifier for flow options")
argparser.add_argument('-f', '--file', dest='filename', help='rules file to open and verify', required=True)
args = argparser.parse_args()

try:
  rules = rule.parse_file(args.filename)
except Exception as e:
  print("invalid file or bad permissions?")
  print(e)
  exit(1)


flowoptions = ["to_server","to_client","from_server","from_client"]
badsids = []
for rule in rules:
    checkRule = True
    if rule.source_port == 'any':
        if rule.dest_port == 'any':
            checkRule = True
        else: # port was a number
            if int(rule.dest_port) <= 1024:
                checkRule = False # don't bother checking, OS won't use these
    elif int(rule.source_port) <= 1024:
        checkRule = False # don't bother checking, OS won't use these
    if False == checkRule:
        continue # don't check
    # otherwise, check the rule
    flowfound = False
    for f in flowoptions:
        try:
            if f in rule.flow:
                flowfound = True
                break
        except:
            # rule has no 'flow' keyword, probably
            break
    if flowfound:
        continue
    else:
        badsids.append(rule.sid)

if len(badsids) > 0:
    print("WARNING: The following rules had a port defined > 1024 and had no flow set")
    for sid in badsids:
        print("sid: ", sid)
    exit(1)
    
