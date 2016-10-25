import numpy as np
import time
import lda
import lda.datasets
import sys

if len(sys.argv) != 3:
    print "input:[the number of topics] [the number of iter]"
    sys.exit(1)

kk = int(sys.argv[1])
nn = int(sys.argv[2])
X = np.loadtxt('/home/ec2-user/data/classinfo/matrix.txt',dtype=np.uint8)

fwl = open("/home/ec2-user/git/statresult/wordslist_dsw.txt","r")
wtol = {}
itow = {}
vocab = []
for line in fwl:
    line = line.strip('\n')
    vocab.append(line)
fwl.close()


start = time.clock()
model = lda.LDA(n_topics=kk, n_iter=nn, random_state=1)
model.fit(X)  # model.fit_transform(X) is also available
end = time.clock()

topic_word = model.topic_word_  # model.components_ also works
n_top_words = 8
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
print model.components_
np.save("lda-"+str(kk)+"-"+str(nn)+"-phi.npy",model.components_)
np.save("lda-"+str(kk)+"-"+str(nn)+"-theta.npy",model.doc_topic_)
print model.nz_
print "running time:",end-start
