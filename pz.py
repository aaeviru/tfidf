import numpy as np
import sys

if len(sys.argv) != 3:
    print "input:theta-file,pz-file"
    sys.exit(1)
a = np.load(sys.argv[1])
np.save(sys.argv[2],[a[:,i].sum() / a.shape[0] for i in range(0,a.shape[1])])
