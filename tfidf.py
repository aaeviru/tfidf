import os
import sys
import math

if len(sys.argv) != 3:
    print "input: folder,type[0/1/2]"
    sys.exit(1)
fq = {}
df = {}
type = int(sys.argv[2])
if type == 0:
    fdf = open("/home/ec2-user/data/classinfo/fq_3.txt")
elif type == 1:
    fdf = open("/home/ec2-user/data/classinfo/fq_2.txt")
elif type == 2:
    fdf = open("/home/ec2-user/data/classinfo/fq_1.txt")

if type > 2:
    for root, dirs, files in os.walk(sys.argv[1]):
        for name in files:
            filename = root + '/' + name
            if filename[len(filename)-1] == 'f':
                fin = open(filename,'r')
                fout = open(filename+'n','w')
                for line in fin:
                    line = line.split(' ')[0]
                    fout.write(line+'\n')
                fin.close()
                fout.close()
    sys.exit(0)

for line in fdf:
    line = line.strip("\n")
    line = line.split(" ")
    df[line[0]] = int(line[1])
fdf.close()

for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if type == 0 and filename[len(filename)-1] == 'q':
            fin = open(filename,'r')
            fout = open(filename+".tfidf","w")
            tfidf = {}
            for line in fin:
                line = line.strip("\n")
                line = line.split(" ")
                tfidf[line[0]] = int(line[1]) * math.log(623.0 / df[line[0]])
            for w in sorted(tfidf, key=tfidf.get, reverse=True):
                fout.write(str(w) + ' ' + str(tfidf[w]) + '\n')
            fout.close()
            fin.close()
        elif type == 1 and filename[len(filename)-1] == 't' and name[0:len(name)-4].isdigit():
            fin = open(filename,'r')
            fout = open(filename+".tfidf","w")
            tfidf = {}
            for line in fin:
                line = line.strip("\n")
                line = line.split(" ")
                tfidf[line[0]] = int(line[1]) * math.log(120.0 / df[line[0]])
            for w in sorted(tfidf, key=tfidf.get, reverse=True):
                fout.write(str(w) + ' ' + str(tfidf[w]) + '\n')
            fout.close()
            fin.close()
        elif type == 2 and name == "fq.txt":
            fin = open(filename,'r')
            fout = open(filename+".tfidf","w")
            tfidf = {}
            for line in fin:
                line = line.strip("\n")
                line = line.split(" ")
                tfidf[line[0]] = int(line[1]) * math.log(8.0 / df[line[0]])
            for w in sorted(tfidf, key=tfidf.get, reverse=True):
                fout.write(str(w) + ' ' + str(tfidf[w]) + '\n')
            fout.close()
            fin.close()

