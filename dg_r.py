#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re
import numpy as np

if len(sys.argv) != 6:
    print "input:topic-folder,cl-flie,cl-folder,zipf-k,type[1/2]"
    sys.exit(1)

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
            clf = sys.argv[3]+'/'+cl[0]+'/'+cl+'.txt.fq.tfidfn'
            if type == 2:
                clf = clf + '2'
            fcl = open(clf,'r')

            tmp = fcl.readlines()
            fcl.close()
            for line in fin:
                if line in tmp[0:10000]:
                    w.append(tmp.index(line))
            fin.close()
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
                clf = sys.argv[3]+'/'+cl[0]+'/'+cl+'.txt.fq.tfidfn'
                if type == 2:
                    clf = clf + '2'
                fcl = open(clf,'r')
                tmp = fcl.readlines()    
                fcl.close()

                rr =  set()
                #qlen = abs(len(w)+np.random.normal(0,2,1))
                qlen = len(w)
                while len(rr) < qlen:
                    dp = int(np.random.zipf(zipf,1))
                    if dp < len(tmp) and dp not in rr:
                        rr.add(dp)
                        print tmp[int(dp)].strip('\n')
                    else:
                        continue
                print

            for i in w:
                tw = ttmmpp[i].strip('\n')
                print tw
                t = t + tw + ' '
            print
            print t
