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
from pythonlib import sysf

inputform = "topic-folder,cl-flie(rand for random),cl-folder,zipf-k(<=1 for non-random,<0 for ldarand type3 only),type[0(tfidf)/1(tfidf2)/2(lsa)/3(lda)],output-folder"
if len(sys.argv) != 7:
    print "input:"+inputform
    sys.exit(1)


outf = sys.argv[6]+'/dg-'+'-'.join(map(lambda x:x.strip('/').split('/')[-1],sys.argv[2:-1]))
fout = sysf.logger(outf,inputform)

clpath = sys.argv[3]
zipf = float(sys.argv[4])
type = int(sys.argv[5])

if type == 2:
    a = np.load('/home/ec2-user/data/classinfo/vt.npy')#lsa result
    s = None
if type == 3:
    #a = np.load('/home/ec2-user/git/statresult/lda-30-2000-phi.npy')
    #s = np.load('/home/ec2-user/git/statresult/lda-30-2000-pz.npy')
    a = np.load('/home/ec2-user/git/statresult/lda-32-1000-top10000-phi.npy')
    s = np.load('/home/ec2-user/git/statresult/lda-32-1000-top10000-pz.npy')

if type == 2:
    wtol = sm.readwl("/home/ec2-user/git/statresult/wordslist_dsw.txt")
    kk = a.shape[0]
elif type == 3:
    wtol = sm.readwl("/home/ec2-user/git/statresult/wordslist_top10000_dsw.txt")
    kk = a.shape[0]
    if zipf < 0:
        fldawl = open('/home/ec2-user/git/statresult/wordslist_top10000_dsw.txt','r')#wordlist for lda
        i = 0
        ltow = {}
        for line in fldawl:
            line = line.strip('\n')
            ltow[i] = line
            i = i + 1
        fldawl.close()
        p = []
        p.append(a[:,0])
        for i in range(1,a.shape[1]):
            p.append(a[:,i]+p[i-1])
        p = np.array(p)
        p = p.transpose()


elif type in (0,1):
    a = None
    s = None
    wtol = None
    kk = None

if sys.argv[2] == 'rand':
    fcl = open('/home/ec2-user/git/tfidf/result/classname.txt','r')
    cll = {}
    if type in (0,1):
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
    elif type in (2,3):
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
        filename = root + '/' + name
        result = None
        if name.isdigit():
            if type == 3 and zipf < 0:
                result = sm.dg3(filename,cll,a,s,p,wtol,ltow,kk)
            else:
                result = sm.dg(filename,cll,clpath,a,s,wtol,kk,zipf,type)
        if result == None:
            continue
        fout.write('@'+root+name+'\n')
        for i in range(0,len(result)-1):
            for j in result[i]:
                fout.write(j+'\n')
            fout.write('\n')
        fout.write(result[-1]+'\n')

