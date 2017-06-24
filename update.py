#!/usr/bin/env python

# Web page with the AMI matrix
# http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html

import requests
import re
from shutil import move
from os import remove

# List of ECS config files to update
files = ['demo.yaml']

amipage = requests.get('http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html')

amiregions = re.findall('((?<=region=).+?(?=#))', amipage.content.decode('utf-8'))
amis = re.findall('((?<=ami=).+?(?="))', amipage.content.decode('utf-8'))

mapping = dict(zip(amiregions, amis))

for file in files:
    newfilename = file + '.new'
    with open(newfilename, 'w') as newfile:
        with open(file) as workingfile:
            for line in workingfile:
                nextline = False
                for region in amiregions:
                    if region in line:
                        newfile.write(line)
                        nextline = True
                    if nextline:
                        line = next(workingfile)
                        line = re.sub('ami-.{8}', mapping[region], line)
                        nextline = False
                newfile.write(line)
    remove(file)
    move(newfilename, file)
