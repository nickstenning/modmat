from __future__ import division

from modmat import ga
from modmat import net

_n = None
_npops = None
_popsize = None

populations = None
fitnesses = None
stats = None

def init(npops, n, popsize):
    global _npops, _n, _popsize
    global populations, fitnesses, stats

    _npops = npops
    _n = n
    _popsize = popsize
    populations = []
    fitnesses = []
    stats = [{}] * _npops

    for i in xrange(_npops):
        pop, fit = ga.init(_n, _popsize)
        populations.append(pop)
        fitnesses.append(fit)

def tick():
    global stats, populations, fitnesses

    for i in xrange(_npops):
        populations[i], fitnesses[i] = ga.tick(populations[i], fitnesses[i])

        stats[i].update({
            'mean_fit': sum(fitnesses[i]) / _popsize,
            'mean_sccs': sum(net.num_sccs_in_array(m) for m in populations[i]) / _popsize
        })

