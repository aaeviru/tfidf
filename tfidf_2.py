import os
import sys
import math

if len(sys.argv) != 2:
    print "input: folder"
    sys.exit(1)
fq = {}
df = {}
fidf = open("/home/ec2-user/data/totalidf_dsw.py")

for line in fidf:
    line = line.strip("\n")
    line = line.split(" ")
    df[line[0]] = float(line[1])
fidf.close()

for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if filename[len(filename)-1] == 'q':
            fin = open(filename,'r')
            fout = open(filename+".tfidfn2","w")
            tfidf = {}
            for line in fin:
                line = line.strip("\n")
                line = line.split(" ")
                tfidf[line[0]] = int(line[1]) * df[line[0]]
            for w in sorted(tfidf, key=tfidf.get, reverse=True):
                fout.write(str(w) + '\n')
            fout.close()
            fin.close()

