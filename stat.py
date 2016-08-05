import os
import sys
import math

s = 0
num = 0
ma = 0
mi = 99999999999999
if len(sys.argv) != 3:
    print "input: folder,type[0/1/2]"
    sys.exit(1)
type = int(sys.argv[2])
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if (type == 0 and filename[len(filename)-1] == 'q') or (type == 1 and filename[len(filename)-1] == 't' and name[0:len(name)-4].isdigit()) or (type == 2 and name == "fq.txt"):
            fin = open(filename,"r")
            l = len(fin.readlines())
            if l > ma:
                ma = l
            if l < mi:
                mi = l
            if l < 1000:
                print filename
            s = s + l
            num = num + 1
            fin.close()
print "max:",ma
print "mim:",mi
print "average:",s * 1.0 / num

