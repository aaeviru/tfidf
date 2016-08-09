#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re
import numpy as np

if len(sys.argv) != 4:
    print "input:topic-folder,cl-folder,type[0/1]"
    sys.exit(1)

wn = 2973096
w = []
for i in range(wn):
    w.append(0)
ave = 0
num = 0
type = int(sys.argv[3])
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if name.isdigit():
            fin = open(filename,'r')
            temp = fin.read()
            fin.close()
            cl = re.findall(r'【国際特許分類第.*版】.*?([A-H][0-9]+?[A-Z])',temp,re.DOTALL)
            if(len(cl) < 1):
                print filename
                break
            print '@'+filename
            cl = cl[0]
            cl = cl[0] + str(int(cl[1:len(cl)-1])) +cl[len(cl)-1]
            fin  = open(filename+'.txt','r')
            if type == 0:
		fcl = open(sys.argv[2]+'/'+cl[0]+'/'+cl+'.txt.fq.tfidfn')
	    else:
		fcl = open(sys.argv[2]+'/'+cl+'.txt')

            tmp = fcl.readlines()
            fcl.close()
            for line in fin:
                if line in tmp:
                    tmpn = tmp.index(line)
                    num = num + 1
                    ave = ave + tmpn
                    w[tmpn] = w[tmpn] + 1
np.savetxt('test.out',w,fmt='%d')
print ave
print num
print 1.0 * ave / num
                
