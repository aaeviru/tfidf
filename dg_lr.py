#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re
import numpy as np

if len(sys.argv) != 4:
    print "input:topic-folder,cl-flie,cl-folder"
    sys.exit(1)

cll = {}
for i in range(0,623):
    cll[i] = np.random.randint(623,size=3)

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
kk = 623

def classof(lines):
    global a,wtol,kk
    vec = np.zeros(kk)
    for line in lines:
        line = line.strip('\n')
        vec = vec + a[:,wtol[line]]
    return vec.argmax()

'''
fcl = open(sys.argv[2],'r')
cll = {}
for line in fcl:
    line = line.strip(' \n')
    line = line.split(' ')
    for w in line:
        cll[w] = list(line)
        cll[w].remove(w)
fcl.close()
'''
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if name.isdigit():
            w = []
            fin  = open(filename+'.txt','r')
            lines = fin.readlines()
            fin.close()
            cl = classof(lines)
            fcl = open(sys.argv[3]+'/'+str(cl))

            tmp = fcl.readlines()
            fcl.close()
            for line in lines:
                if line in tmp[0:10000]:
                    w.append(tmp.index(line))
            r = []
            t = '!'
            rq = np.array(w)
            mean = rq.mean()
            std = rq.std()
            #print mean,std
            if cl not in cll:
                continue
            print '@'+filename
            ttmmpp = list(tmp)
            del tmp
            for tcl in cll[cl]:
                fcl = open(sys.argv[3]+'/'+str(tcl))
                tmp = fcl.readlines()    
                fcl.close()
                dq = np.random.exponential(min(mean,std),abs(len(w)+np.random.normal(0,1,1)))
             #   print dq.mean(),dq.std()
              #  print dq
                rr = []
                for i in dq:
                    if i < len(tmp):
                        print tmp[int(i)].strip('\n')
                print
            for i in w:
                tw = ttmmpp[i].strip('\n')
                print tw
                t = t + tw + ' '
            print
            print t
