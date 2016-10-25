from scipy.stats import entropy as kld
import os
import sys
import math
import re
import numpy as np

if len(sys.argv) != 3:
    print "input:topic-folder,cl-folder"
    print kld([0.1,0.9],[0.9,0.1])
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
kk = 623
ttq = 0
ttp = 0.0

def classof(lines):
    global a,wtol,kk
    vec = np.zeros(kk)
    for line in lines:
        line = line.strip('\n')
        vec = vec + a[:,wtol[line]]
    return vec.argmax()

tn = 0
ttl = 0
w = {}
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        filename = root + '/' + name
        if name.isdigit():
            fin  = open(filename+'.txt','r')
            lines = fin.readlines()
            fin.close()
            tn = tn + len(lines)
            cl = classof(lines)
            fcl = open(sys.argv[2]+'/'+str(cl))

            tmp = fcl.readlines()
            if ttl < len(tmp):
                ttl = len(tmp)
            fcl.close()
            ttq = ttq + 1
            for line in lines:
                ll = tmp.index(line)
                if ll in w:
                    w[ll] = w[ll] + 1
                else:
                    w[ll] = 1
fm = 0.0
for i in range(ttl):
    fm = fm + 1.0/(i+1)
e = []
for i in range(ttl):
    e.append(1.0/(i+1)/fm)
e = np.array(e)

alpha = 0.0000001

for i in range(ttl):
    if i not in w:
        w[i] = alpha/tn
    else:
        w[i] = (1-alpha)*w[i]/tn+alpha/tn

o = np.array(w.values())
print kld(e,o)
print kld(o,e)
