#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re
import numpy as np
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from pythonlib import semantic as sm

if len(sys.argv) != 6:
    print "input:topic-folder,cl-flie,cl-folder,zipf-k,type[1/2]"
    sys.exit(1)

clpath = sys.argv[3]
zipf = float(sys.argv[4])
type = int(sys.argv[5])

if sys.argv[2] == 'rand':
    fcl = open('/home/ec2-user/git/tfidf/result/classname.txt','r')
    cll = {}
    acl = []
    for line in fcl:
        line = line.strip(' \n')
        line = line.split(' ')
        for w in line:
            acl.append(w)
    for i in range(0,623):
        tmpc = []
        for j in range(3):
            tmpc.append(acl[np.random.randint(623)])
        cll[acl[i]] = list(tmpc)
else:
    fcl = open(sys.argv[2],'r')
    cll = {}
    for line in fcl:
        line = line.strip(' \n')
        line = line.split(' ')
        for w in line:
            cll[w] = list(line)
            cll[w].remove(w)
    fcl.close()

for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if name.isdigit():
            result = sm.dg2(filename,cll,clpath,zipf,type)
        if result == None:
            continue
        print '@'+root+name
        for i in range(0,len(result)-1):
            for j in result[i]:
                print j
            print
        print result[-1]

