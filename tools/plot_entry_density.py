import os
import sys
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

fp = np.load(sys.stdin)

N = fp[fp.keys()[0]].shape[0]

neg = np.zeros((N, N))
pos = np.zeros((N, N))

for k, arr in fp.iteritems():
    for i in xrange(N):
        for j in xrange(N):
            if arr[i, j] != 0:
                neg[i, j] += 1

            # if arr[i, j] > 0:
            #     pos[i, j] += 1
            # elif arr[i, j] < 0:
            #     neg[i, j] += 1

matplotlib.rcParams.update({'font.size': 18})

neg /= 8000.0

plt.imshow(neg, interpolation='nearest')
# plt.imshow(pos, interpolation='nearest')
plt.colorbar()

if os.isatty(sys.stdout.fileno()):
    plt.show()
else:
    plt.savefig(sys.stdout, format='png')
