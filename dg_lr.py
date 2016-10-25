#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re
import numpy as np

def vecof2(lines,idf,a,wtol,kk):
    vec = np.zeros(kk)
    for line in lines:
        line = line.strip('\n')
        line = line.split(' ')
        if line[1] in wtol:
            vec = vec + a[:,wtol[line[1]]] * idf[line[1]] * int(line[0])
    return vec/np.linalg.norm(vec)

def vecof(lines,a,wtol,kk):
    vec = np.zeros(kk)
    for line in lines:
        line = line.strip('\n')
        vec = vec + a[:,wtol[line]]
    return vec


def readwl(wlpath):
    fwl = open(wlpath,"r")
    wtol = {}
    itow = {}
    i = 0
    for line in fwl:
        line = line.strip('\n')
        wtol[line] = i
        i = i + 1
    fwl.close()
    return wtol


def classof(lines,a,wtol,kk):
    vec = np.zeros(kk)
    for line in lines:
        line = line.strip('\n')
        vec = vec + a[:,wtol[line]]
    return vec.argmax()

def dg(root,name,cll,clpath,zipf,a,wtol,kk):
    filename = root + '/' + name
    w = []
    fin  = open(filename+'.txt','r')
    lines = fin.readlines()
    fin.close()
    cl = classof(lines,a,wtol,kk)
    fcl = open(clpath+'/'+str(cl))
    tmp = fcl.readlines()
    fcl.close()
    for line in lines:
        if line in tmp[0:10000]:
            w.append(tmp.index(line))
    rq = np.array(w)
    mean = rq.mean()
    std = rq.std()
    #print mean,std
    if cl not in cll:
        return None
    ttmmpp = list(tmp)
    del tmp
    result = []
    for tcl in cll[cl]:
        fcl = open(clpath+'/'+str(tcl))
        tmp = fcl.readlines()    
        fcl.close()
        rr =  set()
        q = []
        #qlen = abs(len(w)+np.random.normal(0,2,1))
        qlen = len(w)
        while len(rr) < qlen:
            dp = int(np.random.zipf(zipf,1))
            if dp < len(tmp) and dp not in rr:
                rr.add(dp)
                q.append(tmp[int(dp)].strip('\n'))
            else:
                continue
        result.append(q)
    q = []
    t = '!'
    for i in w:
        tw = ttmmpp[i].strip('\n')
        q.append(tw)
        t = t + tw + ' '
    result.append(q)
    result.append(t)
    return result

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print "input:topic-folder,cl-flie,cl-folder zipf-p"
        sys.exit(1)

    zipf = float(sys.argv[4])
    wtol = readwl("/home/ec2-user/git/statresult/wordslist_dsw.txt")
    a = np.load('/home/ec2-user/data/classinfo/vt.npy')#lsa result
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
                result = dg(root,name,cll,clpath,zipf,a,wtol,kk)
                if result == None:
                    continue
                print '@'+root+name
                for i in range(0,len(result)-1):
                    for j in result[i]:
                        print j
                    print
                print result[-1]
