from __future__ import absolute_import, print_function


import argparse
import os
import json
import sys

import numpy as np

from modmat import parallel
from modmat.printer import Printer

parser = argparse.ArgumentParser(description="Evolve randomly seeded matrices for stability")

parser.add_argument('-n', metavar='N', type=int, default=25,
                    help='size of matrices')
parser.add_argument('-p', '--popsize', metavar='popsize', type=int, default=1000,
                    help='size of population')
parser.add_argument('-g', '--generations', metavar='ngens', type=int, default=2000,
                    help='number of generations to run for')
parser.add_argument('-k', '--knockout', action='store_true', default=False,
                    help='use knockout fitness rather than default eigvals fitness')
parser.add_argument('datadir',
                    help='output data directory')

def print_tick(printer, stats):
    for i, s in enumerate(stats):
        to_print = {
            'summary': "%10.4g %10.4g %10.4g\n" % (s['mean_fit'], s['mean_hamm'], s['mean_sccs']),
            'sccs_hist': ("%5d " * len(s['sccs_hist']) + "\n") % tuple(s['sccs_hist']),
        }

        if 'net' in s:
            to_print['net'] = s['net']

        printer.register(i, to_print)

    printer.tick()

def save_populations(populations, filename):
    all_arrays = {}

    for i, p in enumerate(populations):
        for j, a in enumerate(p):
            all_arrays['pop%d_arr%d' % (i, j)] = a

    np.savez(filename, **all_arrays)

def save_args(args):
    fname = os.path.join(args.datadir, 'args.json')

    with open(fname, 'w') as fp:
        json.dump(vars(args), fp, indent=2)

def main():
    args = parser.parse_args()
    fitness = 'knockout' if args.knockout else 'eigvals'

    printer = Printer(args.datadir)

    save_args(args)

    parallel.init(1, args.n, args.popsize, fitness=fitness)

    save_populations(parallel.populations, os.path.join(args.datadir, 'arrays_initial.npz'))

    for i in xrange(args.generations):
        print("Generation %d" % i, file=sys.stderr)

        print_nets = True if i == args.generations - 1 else False

        parallel.tick(print_nets=print_nets,
                      fitness=fitness)
        print_tick(printer, parallel.stats)

    save_populations(parallel.populations, os.path.join(args.datadir, 'arrays_final.npz'))



if __name__ == '__main__':
    main()
