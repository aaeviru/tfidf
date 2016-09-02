#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re
import numpy as np

if len(sys.argv) != 5:
    print "input:topic-folder,cl-flie,cl-folder,type[0/1]"
    sys.exit(1)

type = int(sys.argv[4])
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
            fin = open(filename,'r')
            temp = fin.read()
            fin.close()
            cl = re.findall(r'【国際特許分類第.*版】.*?([A-H][0-9]+?[A-Z])',temp,re.DOTALL)
            if(len(cl) < 1):
                print filename
                break
            cl = cl[0]
            cl = cl[0] + str(int(cl[1:len(cl)-1])) +cl[len(cl)-1]
            w = []
            fin  = open(filename+'.txt','r')
            if type == 0:
		fcl = open(sys.argv[3]+'/'+cl[0]+'/'+cl+'.txt.fq.tfidfn')
	    else:
		fcl = open(sys.argv[3]+'/'+cl+'.txt')

            tmp = fcl.readlines()
            fcl.close()
            for line in fin:
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
                if type == 0:
                    fcl = open(sys.argv[3]+'/'+tcl[0]+'/'+tcl+'.txt.fq.tfidfn')
                else:
                    fcl = open(sys.argv[3]+'/'+tcl+'.txt')
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
