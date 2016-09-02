import re
import os
import sys
import numpy as np
from numpy import linalg as nplg
from scipy import linalg as sclg
from scipy.sparse import linalg
from scipy import sparse as sp

if len(sys.argv) != 2:
    print "input: bk file\n"
    exit(0)

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
s = 1


for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
            filename = root + '/' + name
            if filename[len(filename)-1] == 'n':
                vec = np.zeros(kk)
                fng = open(filename,"r")
                lines = fng.readlines()
                fng.close()
                cllen = len(lines)
                if cllen>1000:
                    cllen = 1000

                for line in lines[0:cllen]:
                    term = line.strip('\n')
                    if term in wtol:
                        tmp = s * a[:,wtol[term]]
                        vec = vec + tmp
                mmax = vec.argmax()
                print filename,mmax
                for line in lines[0:100]:
                    term = line.strip('\n')
                    if term in wtol:
                        print term,a[:,wtol[term]][mmax],a[:,wtol[term]].max()
                #attack('end')
                print
                print
                print
                print
                print
