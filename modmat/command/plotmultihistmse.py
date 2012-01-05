from __future__ import division

import os
import sys

from matplotlib import pyplot as plt
import numpy as np

FIRST = 0
LAST = -1

GENERATION = LAST

def main():
    filenames = sys.argv[1:]
    data = []

    for fn in filenames:
        d = np.loadtxt(open(fn), unpack=True)
        data.append(d)

    data = np.array(data)

    x = range(1, len(data[0][...,GENERATION]) + 1)

    for i, d in enumerate(data):
        plt.plot(x, d[...,GENERATION], 'k', alpha=0.05)

    pop_gens = data[...,...,GENERATION]

    max_ = pop_gens.max(axis=0)
    min_ = pop_gens.min(axis=0)
    mean = pop_gens.mean(axis=0)

    # Std error in mean = sample stddev / sqrt(n)
    serr = pop_gens.std(axis=0, ddof=1) / np.sqrt(len(pop_gens))

    plt.plot(x, mean)
    plt.plot(x, max_, '--k', alpha=0.4)
    plt.plot(x, min_, '--k', alpha=0.4)
    plt.fill_between(x, mean - serr, mean + serr, alpha=0.1)

    plt.semilogy()

    if os.isatty(sys.stdout.fileno()):
        plt.show()
    else:
        plt.savefig(sys.stdout, format='png')

if __name__ == '__main__':
    main()
