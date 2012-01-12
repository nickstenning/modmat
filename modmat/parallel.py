from __future__ import division

import numpy as np

from modmat import ga
from modmat import net
from modmat import util

_n = None
_npops = None
_popsize = None

populations = None
fitnesses = None
stats = None

def init(npops, n, popsize, fitness='eigvals'):
    global _npops, _n, _popsize
    global populations, fitnesses, stats

    _npops = npops
    _n = n
    _popsize = popsize
    populations = []
    fitnesses = []
    stats = [None] * _npops

    for i in xrange(_npops):
        pop, fit = ga.init(_n, _popsize, fitness=fitness)
        populations.append(pop)
        fitnesses.append(fit)

def tick(print_nets=False, fitness='eigvals'):
    global stats, populations, fitnesses

    for i in xrange(_npops):
        populations[i], fitnesses[i] = ga.tick(populations[i], fitnesses[i], fitness=fitness)

        sccs = [net.sccs_in_array(m) for m in populations[i]]
        sccs_flat = [x for s in sccs for x in s] # sccs across population
        sccs_hist = util.histogram(sccs_flat)
        sccs_hist = util.truncate_or_pad(sccs_hist, _n + 1, 0)[1:]

        hamm = util.mean_hamming(populations[i])

        stats[i] = {
            'mean_fit': sum(fitnesses[i]) / _popsize,
            'mean_sccs': sum([len(s) for s in sccs]) / _popsize,
            'mean_hamm': hamm,
            'sccs_hist': sccs_hist
        }

        if print_nets:
            rand_net = populations[i][np.random.randint(_popsize)]
            stats[i]['net'] = net.array_to_dot(rand_net)

