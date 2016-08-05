import os
import sys

if len(sys.argv) != 3:
    print "input: folder,type[0/1/2]"
    sys.exit(1)
fq = {}
type = int(sys.argv[2])
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if type == 0 and filename[len(filename)-1] == 'q':
            fin = open(filename,'r')
            for line in fin:
                line = line.strip("\n")
                line = line.split(" ")
                if line[0] in fq:
                    fq[line[0]] = fq[line[0]] + 1
                else:
                    fq[line[0]] = 1
            fin.close()
        elif type == 1 and filename[len(filename)-1] == 't' and name[0:len(name)-4].isdigit():
            fin = open(filename,'r')
            for line in fin:
                line = line.strip("\n")
                line = line.split(" ")
                if line[0] in fq:
                    fq[line[0]] = fq[line[0]] + 1
                else:
                    fq[line[0]] = 1
            fin.close()
        elif type == 2 and name == "fq.txt":
            fin = open(filename,'r')
            for line in fin:
                line = line.strip("\n")
                line = line.split(" ")
                if line[0] in fq:
                    fq[line[0]] = fq[line[0]] + 1
                else:
                    fq[line[0]] = 1
            fin.close()

if type == 0:
    fout = open(sys.argv[1]+"/fq_3.txt",'w')
elif type == 1:
    fout = open(sys.argv[1]+"/fq_2.txt",'w')
else:
    fout = open(sys.argv[1]+"/fq_1.txt",'w')

for w in sorted(fq, key=fq.get, reverse=True):
    fout.write(str(w) + ' ' + str(fq[w]) + '\n')
fout.close()
