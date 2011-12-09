from __future__ import division, absolute_import

import argparse
import sys

from modmat import ga
from modmat import net

parser = argparse.ArgumentParser(description="Evolve randomly seeded matrices for stability")

parser.add_argument('-n', metavar='N', type=int, default=100,
                    help='size of matrices')
parser.add_argument('-p', '--popsize', metavar='popsize', type=int, default=100,
                    help='size of population')
parser.add_argument('-g', '--generations', metavar='ngens', type=int, default=500,
                    help='number of generations to run for')

def main():
    args = parser.parse_args()

    pop, fit = ga.init(args.n, args.popsize)

    for _ in xrange(args.generations):
        pop, fit = ga.tick(pop, fit)

        mean_fit = sum(fit) / args.popsize
        mean_sccs = sum(net.num_sccs_in_array(m) for m in pop) / args.popsize
        print "%10.4g %10.4g" % (mean_fit, mean_sccs)
        sys.stdout.flush()


if __name__ == '__main__':
    main()
