import os
import sys
import math
from sklearn.neighbors import BallTree

if len(sys.argv) != 4:
    print "input: folder,type[0/1/2/3(lsa),dsfunc[0(far)/1(near)]]"
    sys.exit(1)
type = int(sys.argv[2])
dsf = int(sys.argv[3])
c = set()
x = {}
last = 1000
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if (type == 0 and filename[len(filename)-1] == 'f' and filename[len(filename)-7] == 'q') or (type == 1 and filename[len(filename)-1] == 'f' and name[0:len(name)-10].isdigit()) or (type == 2 and name == "fq.txt.tfidf") or (type == 3):
            fin = open(filename,"r")
            l = fin.readlines()
            fin.close()
            if len(l) < 1000:
                continue 
            if type == 0:#r3
                cl = name[0:len(name)-13]
            elif type == 1:#r2
                cl = root[len(root)-1] + name[0:len(name)-10]
            elif type == 2:#r1
                cl = root[len(root)-1]
            elif type == 3:#lsa
                cl = name
            if len(l) > last:
                x[cl] = l[0:last]
            else:
                x[cl] = l
            c.add(cl)
#            x[cl] = l[0:1000]

def inn(a,b):
    tmp = len([val for val in a if val in b])
    return 1.0*tmp/(len(a)+len(b)-tmp)
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
                cc.remove(i)
    if len(cc) > 0:
        w = []
        for j in range(2):
            for tt in cc:
                w.append(tt)
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


