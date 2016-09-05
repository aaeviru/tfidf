#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re
import numpy as np

if len(sys.argv) != 3:
    print "input:topic-folder,cl-folder"
    sys.exit(1)

fwl = open("/home/ec2-user/git/statresult/wordslist_dsw.txt","r")
wtol = {}
itow = {}
i = 0
for line in fwl:
    line = line.strip('\n')
    wtol[line] = i
    itow[i] = line
    i = i + 1
fwl.close()

a = np.load('/home/ec2-user/data/classinfo/vt.npy')
wn = 2973096
w = []
for i in range(wn):
    w.append(0)

kk = 623
num = 0
ave = 0

def classof(lines):
    global a,wtol,kk
    vec = np.zeros(kk)
    for line in lines:
        line = line.strip('\n')
        vec = vec + a[:,wtol[line]]
    return vec.argmax()

for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if name.isdigit():
            fin  = open(filename+'.txt','r')
            lines = fin.readlines()
            fin.close()
            cl = classof(lines)
            fcl = open(sys.argv[2]+'/'+str(cl))

            tmp = fcl.readlines()
            fcl.close()
            for line in lines:
                if line in tmp:
                    tmpn = tmp.index(line)
                    num = num + 1
                    ave = ave + tmpn
                    w[tmpn] = w[tmpn] + 1
np.savetxt('test-lsa.out',w,fmt='%d')
print ave
print num
print 1.0 * ave / num

