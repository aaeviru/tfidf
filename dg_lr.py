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
    print "input:topic-folder,cl-flie,cl-folder,zipf-a,type[0(lsa)/1(lda)]"
    sys.exit(1)

zipf = float(sys.argv[4])
wtol = sm.readwl("/home/ec2-user/git/statresult/wordslist_dsw.txt")
type = int(sys.argv[5])
if type == 0:
    a = np.load('/home/ec2-user/data/classinfo/vt.npy')#lsa result
    s = 1
else:
    a = np.load('/home/ec2-user/git/statresult/lda-30-2000-phi.npy')
    s = np.load('/home/ec2-user/git/statresult/lda-30-2000-pz.npy')

kk = a.shape[0]
clpath = sys.argv[3]

if sys.argv[2] == 'rand':
    cll = {}
    for i in range(0,kk):
        cll[i] = np.random.randint(kk,size=3)
else:
    fcl = open(sys.argv[2],'r')
    cll = {}
    for line in fcl:
        line = line.strip(' \n')
        line = line.split(' ')
        for w in line:
            ww = int(w)
            cll[ww] = list(line)
            cll[ww].remove(w)
    fcl.close()

for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        if name.isdigit():
            if type == 0:
                result = sm.dg(root,name,cll,clpath,zipf,a,wtol,kk)
            else:
                result = sm.dg3(root,name,cll,clpath,zipf,a,s,wtol,kk)
            if result == None:
                continue
            print '@'+root+name
            for i in range(0,len(result)-1):
                for j in result[i]:
                    print j
                print
            print result[-1]
