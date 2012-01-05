from __future__ import absolute_import, print_function


import argparse
import sys

from modmat import parallel
from modmat.printer import Printer

parser = argparse.ArgumentParser(description="Evolve randomly seeded matrices for stability")

parser.add_argument('-n', metavar='N', type=int, default=25,
                    help='size of matrices')
parser.add_argument('-p', '--popsize', metavar='popsize', type=int, default=1000,
                    help='size of population')
parser.add_argument('-g', '--generations', metavar='ngens', type=int, default=2000,
                    help='number of generations to run for')
parser.add_argument('datadir',
                    help='output data directory')

def print_tick(printer, stats):
    for i, s in enumerate(stats):
        printer.register(i, {
            'summary': "%10.4g %10.4g\n" % (s['mean_fit'], s['mean_sccs']),
            'sccs_hist': ("%5d " * len(s['sccs_hist']) + "\n") % tuple(s['sccs_hist'])
        })

    printer.tick()

def main():
    args = parser.parse_args()
    printer = Printer(args.datadir)

    parallel.init(1, args.n, args.popsize)

    for _ in xrange(args.generations):
        print("Generation %d" % i, file=sys.stderr)

        parallel.tick()
        print_tick(printer, parallel.stats)


if __name__ == '__main__':
    main()
