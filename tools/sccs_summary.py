from __future__ import division

import sys
import numpy as np

fp = np.load(sys.stdin)

N = fp[fp.keys()[0]].shape[0]

from modmat import net

scc_count = [len(net.sccs_in_array(arr)) for k, arr in fp.iteritems()]
mean_sccs = sum(scc_count) / len(scc_count)
serr_sccs = np.std(scc_count, ddof=1) / np.sqrt(len(scc_count))

tot = 0
nonz = 0
for k, arr in fp.iteritems():
    for i in xrange(N):
        for j in xrange(N):
            tot += 1
            if arr[i, j] != 0:
                nonz += 1


print "Mean number of SCCS: %g +- %g" % (mean_sccs, serr_sccs)
print "Mean entry density: %g" % (nonz/tot)
