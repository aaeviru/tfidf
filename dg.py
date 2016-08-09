#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re

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
            print '@'+filename
            cl = cl[0]
            cl = cl[0] + str(int(cl[1:len(cl)-1])) +cl[len(cl)-1]
            w = set()
            fin  = open(filename+'.txt','r')
            if type == 0:
		fcl = open(sys.argv[3]+'/'+cl[0]+'/'+cl+'.txt.fq.tfidfn')
	    else:
		fcl = open(sys.argv[3]+'/'+cl+'.txt')

            tmp = fcl.readlines()
            fcl.close()
            for line in fin:
                if line in tmp:
                    w.add(tmp.index(line))
            r = {}
            t = '!'
            for i in w:
                r[i] = []
                tw = tmp[i].strip('\n')
                r[i].append(tw)
            for tcl in cll[cl]:
                if type == 0:
                    fcl = open(sys.argv[3]+'/'+tcl[0]+'/'+tcl+'.txt.fq.tfidfn')
                else:
                    fcl = open(sys.argv[3]+'/'+tcl+'.txt')
                tmp = fcl.readlines()    
                fcl.close()
                for i in w:
                    if i < len(tmp):
                        r[i].append(tmp[i].strip('\n'))
            for i in r:
                if len(r[i]) == 4:
                    for j in r[i]:
                        print j
                    t = t + r[i][0] + ' '
                    print
            print t
            break
                
