from __future__ import division

import os
import sys

import matplotlib
from matplotlib import pyplot as plt
import numpy as np

FIRST = 0
LAST = -1

GENERATION = FIRST

def plot_generation(data, generation, fmt):
    x = range(1, len(data[0][...,generation]) + 1)

    pop_gens = data[...,...,generation]

    mean = pop_gens.mean(axis=0) / 8000

    # Std error in mean = sample stddev / sqrt(n)
    serr = pop_gens.std(axis=0, ddof=1) / np.sqrt(len(pop_gens))
    serr /= 8000

    plt.plot(x, mean, fmt, label="gen %d" % (generation + 1))

    if fmt[0] == 'r':
        fc = 'red'
    elif fmt[0] == 'g':
        fc = 'green'
    else:
        fc = 'blue'

    plt.fill_between(x, mean - serr, mean + serr, alpha=0.1, facecolor=fc)

def main():
    matplotlib.rcParams.update({'font.size': 18})

    filenames = sys.argv[1:]
    data = []

    for fn in filenames:
        d = np.loadtxt(open(fn), unpack=True)
        data.append(d)

    data = np.array(data)

    plot_generation(data, 0,    'b-')
    plot_generation(data, 399,  'g--')
    plot_generation(data, 1999, 'r:')

    plt.legend()
    plt.axes().set_xlim(0, len(data[0][...,0]))
    plt.semilogy()

    plt.axes().set_ylabel('fractional frequency')
    plt.axes().set_xlabel('SCC size')

    if os.isatty(sys.stdout.fileno()):
        plt.show()
    else:
        plt.savefig(sys.stdout, format='png')

if __name__ == '__main__':
    main()
