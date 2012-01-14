from __future__ import division

import numpy as np

from modmat import ga

N = 25
POPSIZE = 100000

def main():
    pop = []

    for i in xrange(POPSIZE):
        pop.append(ga._random_matrix(N))

    pop_eigs = [np.linalg.eigvals(m) for m in pop]

    diff = [np.linalg.norm(pop_eigs[0] - pop_eigs[i]) for i in xrange(1, POPSIZE)]
    mean_diff = np.mean(diff)
    serr_diff = np.std(diff, ddof=1) / np.sqrt(len(diff))

    children = []
    for i in xrange(POPSIZE // 2):
        children.extend(ga._matrix_crossover(pop[2*i], pop[2*i + 1]))

    child_eigs = [np.linalg.eigvals(m) for m in children]

    diff_xover = [np.linalg.norm(child_eigs[i] - pop_eigs[i]) for i in xrange(POPSIZE)]
    mean_diff_xover = np.mean(diff_xover)
    serr_diff_xover = np.std(diff_xover, ddof=1) / np.sqrt(len(diff_xover))

    print "distance between random: %g +- %g" % (mean_diff, serr_diff)
    print "distance between parent/child: %g +- %g" % (mean_diff_xover, serr_diff_xover)

if __name__ == '__main__':
    main()
