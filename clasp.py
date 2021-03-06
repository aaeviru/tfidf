import os
import sys
import math
from os import path
from scipy import spatial
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from pythonlib import semantic as sm
from pythonlib import sysf
import numpy as np

inputform = "cl-folder,stype[num of lsa classes][0(tfidf)/1(tfidf2)/2(lsa)/3(lda)],dsfunc[0(far)/1(near)/2(cos-far)/3(cos-near)],level[1(4)/2(8)...],output-folder"


if len(sys.argv) != 6:
    print "input:"+inputform
    sys.exit(1)

outf = sys.argv[5]+'/b'+'-'.join(map(lambda x:x.strip('/').split('/')[-1],sys.argv[2:-1]))
fout = sysf.logger(outf,inputform)

kk = 0
if len(sys.argv[2]) > 1:
    stype = int(sys.argv[2][0])
    kk = int(sys.argv[2][1:])
else:
    stype = int(sys.argv[2])

level = int(sys.argv[4])
dsf = int(sys.argv[3])
c = set()
x = {}
last = 1000

if stype == 2:
    a = np.load('/home/ec2-user/data/classinfo/vt.npy')#lsa result
    if kk > 0:
        a = a[0:kk]
    wtol = sm.readwl("/home/ec2-user/git/statresult/wordslist_dsw.txt")
    s = None
if stype == 3:
    a = np.load('/home/ec2-user/git/statresult/lda-64-2000-top1000-phi.npy')
    s = np.load('/home/ec2-user/git/statresult/lda-64-2000-top1000-pz.npy')
    wtol = sm.readwl("/home/ec2-user/git/statresult/wordslist_dsw_top1000.txt")
if stype in (2,3):
    kk = a.shape[0]


for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if (stype == 0 and filename[-1] == 'n' and name[0] >= 'A' and name[0] <= 'H') or (stype == 1 and filename[-1] == '2' and name[1] >= '0' and name[1] <= '9') or stype in (2,3):
            fin = open(filename,"r")
            l = fin.readlines()
            fin.close()
            if len(l) < 1000:
                continue 
            if len(l) > last:
                l = l[:last]
            if stype == 0:#tfidf
                cl = name[0:len(name)-14]
            elif stype == 1:#tfidf2
                cl = name[0:len(name)-15]
            elif stype == 2:#lsa
                cl = name
                if int(cl) >= kk:
                    continue
            elif stype == 3:#lda
                cl = name
            if dsf in (0,1):
                x[cl] = l
            else:
                x[cl] = sm.vecof0(l,a,s,wtol,kk)
            c.add(cl)
#            x[cl] = l[0:1000]

if dsf in (0,1):
    def inn(a,b):
        tmp = len([val for val in a if val in b])
        return 1.0*tmp/(len(a)+len(b)-tmp)
else:
    def inn(a,b):
	return spatial.distance.cosine(a,b)

def inm(a,b):
    ssum = 0
    num = 0
    for i in a:
	for j in b:
	    num = num + 1
	    ssum = ssum + inn(i,j)
    return 1.0*ssum/num

def layout(c,y):#c:topic set,y: sim result
    cc = set(c)
    z = []
    if dsf in (0,3):
        rev = False
    else:
        rev = True
    for w in sorted(y, key=y.get,reverse = rev):
        check = 0
        for i in w:
            if i not in cc:
                check = 1
                break
        if check == 0 :
            z.append(w)
            for i in w:
                if i in cc:
                    cc.remove(i)
    if len(cc) > 0:
        w = ()
        for tt in cc:
            w = w + (tt,tt)
        z.append(w)
    return z

y = {}
for i in x:
    for j in x:
        if i < j:
            y[(i,j)] = inn(x[i],x[j])

z = layout(c,y)

def cal(x,z):#x:term vector,z:result in last level
    y = {}
    for i in z:
        for j in z:
            if i < j:
                y[i+j] = inm([x[i[k]] for k in range(len(i))],[x[j[k]] for k in range(len(j))])
    return y
for i in range(0,level):    
    y = cal(x,z)
    z = layout(c,y)       
for i in z:
    for j in i:
        fout.write(j+' ')
    fout.write('\n')
