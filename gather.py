import os
import sys

if len(sys.argv) != 3:
    print "input: folder,type[0(b)/1(s)]"
    sys.exit(1)
fq = {}
type = int(sys.argv[2])
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if filename[len(filename)-1] == 'q':
            if type == 0:
                fin = open(filename,'r')
                for line in fin:
                    line = line.strip("\n")
                    line = line.split(" ")
                    if line[0] in fq:
                        fq[line[0]] = fq[line[0]] + int(line[1])
                    else:
                        fq[line[0]] = int(line[1])
                fin.close()
            else :
                sc = int(name[1:len(name)-8])
                fin = open(filename,'r')
                if sc in fq:
		    for line in fin:
			line = line.strip("\n")
			line = line.split(" ")
			if line[0] in fq[sc]:
			    fq[sc][line[0]] = fq[sc][line[0]] + int(line[1])
			else:
			    fq[sc][line[0]] = int(line[1])
                    
                else:
                    fq[sc] = {}
		    for line in fin:
			line = line.strip("\n")
			line = line.split(" ")
			fq[sc][line[0]] = int(line[1])
                fin.close()

if type == 0:
    fout = open(sys.argv[1]+"/fq.txt",'w')
    for w in sorted(fq, key=fq.get, reverse=True):
        fout.write(str(w) + ' ' + str(fq[w]) + '\n')
    fout.close()
else:
    for f in fq:
        fout = open(sys.argv[1] + '/' + str(f) + '.txt','w')
        for w in sorted(fq[f], key=fq[f].get, reverse=True):
            fout.write(str(w) + ' ' + str(fq[f][w]) + '\n')
        fout.close()
