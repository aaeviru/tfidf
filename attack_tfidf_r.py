import re
import os
import sys
import numpy as np
from numpy import linalg as nplg
from scipy import linalg as sclg
from scipy.sparse import linalg
from scipy import sparse as sp


if len(sys.argv) != 3:
    print "input: bk file,type[0/1]\n"
    exit(0)
type = int(sys.argv[2])
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
s = np.load('/home/ec2-user/data/classinfo/sigma.npy')
kk = 623
#s = 1 / s
s = 1
total = -1
hit = 0
notin = 0
maxnum = 0
maxnum_1 = 0
aver1 = 0.0;
aver2 = 0.0;
aver3 = 0.0;
aver4 = 0.0;

vec = np.zeros(kk)
fng = open(sys.argv[1],"r")
query = []
rquery = []
sq = []
qqq = {}
mqqq = {}
for i in range(4):
    qqq[i] = 0
    mqqq[i] = 0
def attack(fn):
    global vec,aver1,aver2,aver3,aver4,qch,query,rquery,bk,total,hit,a,maxnum,maxnum_1,totalterm
    if vec.max() < 0.0000000000001:
        print vec.max()
        print fn
    else:
        total = total + 1
        mmax = vec.argmax()
        mmax_1 = vec.max()
        check = -1
        checkp = -1
        i = 0
        mt = []
        for sq in query:
            tmp = np.zeros(kk)
            for term in sq:
                if term in wtol:
                    tmp = tmp + (s * a[:,wtol[term]])
            for term in sq:
                if type == 1:
                    print term,(s * a[:,wtol[term]])[mmax],a[:,wtol[term]][tmp.argmax()]
            if type == 1:
                print i,tmp[mmax],len(sq),vec[tmp.argmax()],tmp.argmax(),tmp.max(),mmax
                raw_input()
            #tmp = tmp / nplg.norm(tmp)
            mt.append(tmp.max())
            if tmp[mmax] > check:
                check = tmp[mmax]
                checkp = i
            i = i + 1
        mqqq[np.array(mt).argmax()] = mqqq[np.array(mt).argmax()] +1
        qqq[checkp] = qqq[checkp] + 1
        vec = np.zeros(kk)
#    print len(tt),len(rquery)
#    for i in range(0,len(tt)):
#        print rquery[i],tt[i]

for line in fng:
    if line[0] == '@':
        if total >= 0:
            attack(line)
        if total < 0:
            total = 0
        query = []
    elif len(line) < 2:
        query.append(sq)
        sq = []
    elif line[0] == '!':
        pass
    else:
        term = line.strip('\n')
        if term in wtol:
            sq.append(term)
            tmp = s * a[:,wtol[term]]
            vec = vec + tmp
attack('end')


print "total:",total
for i in range(0,4):
    print str(i)+':'+str(qqq[i]),1.0*qqq[i]/total
    print 'mqqq'+str(i)+':'+str(qqq[i]),1.0*qqq[i]/total
