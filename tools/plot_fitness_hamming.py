from __future__ import division

import os
import sys

import matplotlib
from matplotlib import pyplot as plt
import numpy as np

def plot_set(data, fmt='b', ploton=plt):
    x = np.arange(len(data[0]))

    for i, d in enumerate(data):
        plt.plot(x, d, 'k', alpha=0.05)

    mean = data.mean(axis=0)
    # Std error in mean = sample stddev / sqrt(n)
    serr = data.std(axis=0, ddof=1) / np.sqrt(len(data[:,0]))

    plt.plot(x, mean, fmt)

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

    fitnesses = data[...,0,...]
    hamming = data[...,1,...]

    plot_set(fitnesses)

    ax1 = plt.axes()
    ax2 = ax1.twinx()

    plot_set(hamming, 'r', ploton=ax2)

    ax1.set_xlabel('generation')
    # ax1.set_xlim(0, 600)

    ax1.set_ylabel('fitness')
    ax2.set_ylabel('mean hamming distance')

    plt.subplots_adjust(right=0.85)


    if os.isatty(sys.stdout.fileno()):
        plt.show()
    else:
        plt.savefig(sys.stdout, format='png')

if __name__ == '__main__':
    main()
