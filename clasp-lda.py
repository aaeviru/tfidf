import os
import sys
import math
from sklearn.neighbors import BallTree
from scipy import spatial
from dg_lr import *

if len(sys.argv) != 3:
    print "input:cl-folder,dsfunc[0(far)/1(near)]]"
    sys.exit(1)


a = np.load('/home/ec2-user/data/classinfo/vt.npy')#lsa result
kk = a.shape[0]
wtol = readwl("/home/ec2-user/git/statresult/wordslist_dsw.txt")

dsf = int(sys.argv[2])
c = set()
x = {}
last = 1000
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        fin = open(filename,"r")
        l = fin.readlines()
        fin.close()
        if len(l) < 1000:
            continue 
        cl = name
        if len(l) > last:
            x[cl] = vecof(l[0:last],a,wtol,kk)
        else:
            x[cl] = vecof(l,a,wtol,kk)
        c.add(cl)
#            x[cl] = l[0:1000]

del a,wtol,kk

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

y = {}
for i in x:
    for j in x:
        if i < j:
            y[(i,j)] = inn(x[i],x[j])
def layout(c,y):
    cc = set(c)
    z = []         
    if dsf == 0:
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
        for tt in cc:
            w = (tt,tt)
        print w
        z.append(w)
    return z
z = layout(c,y)
y = {}
for i in z:
    for j in z:
        if i < j:
            y[i+j] = inm((x[i[0]],x[i[1]]),(x[j[0]],x[j[1]]))

z = layout(c,y)       
for i in z:
    for j in i:
        sys.stdout.write(j+' ')
        sys.stdout.flush()
    print


