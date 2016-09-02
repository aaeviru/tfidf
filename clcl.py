import re
import os
import sys
import numpy as np
from numpy import linalg as nplg
from scipy import linalg as sclg
from scipy.sparse import linalg
from scipy import sparse as sp


#cll = []
#fcl = open("/home/ec2-user/git/ptclass/log/matrix.txt","r")
#for line in fcl:
#    lenth = len(line)
#    if lenth<10:
#        break
#    cll.append(line[33:lenth-4])

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
#s = np.load('/home/ec2-user/data/classinfo/sigma.npy')
kk = 623
#s = 1 / s
#s = s.reshape(kk,1)
#a = s * a
#del s
lenth = len(a[0])
outpt = '/home/ec2-user/data/lsaclass/'
for i in range(0,kk):
    fout = open(outpt+str(i),'w')
    b = a[i].argsort()
    for j in range(lenth-1,-1,-1):
        fout.write(itow[b[j]]+'\n')
    fout.close()
