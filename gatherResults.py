from os import listdir
from os.path import isfile, join
import numpy as np

onlyfiles = [ f for f in listdir('./') if isfile(join('./',f)) ]
l = []
for name in onlyfiles:
    try:
        f = open(name)
        l.append(float(f.read().split('\n')[2]))
    except:
        continue

l = np.asarray(l[:-1], dtype=float)
m = np.asarray([np.min(l[:i+1]) for i in range(l.shape[0])])
lm = np.log10(m - 0.39788735773)
print lm[:200]
