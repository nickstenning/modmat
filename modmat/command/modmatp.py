from __future__ import absolute_import, division, print_function

import sys
from IPython.parallel import Client

from modmat import parallel
from modmat.printer import Printer
from modmat.command.modmat import parser, print_tick

parser.add_argument('-i', '--iprofile',
                    help='IPython parallel profile to use', default='default')
parser.add_argument('-q', '--npops', type=int, default=20,
                    help='number of populations to simulate')

def main():
    args = parser.parse_args()

    printer = Printer(args.datadir, args.npops)

    rc = Client(profile=args.iprofile)
    nc = len(rc)

    dv = rc[:]
    dv.block = True

    print("# Running on %s processes" % nc, file=sys.stderr)

    dv.execute('from modmat import parallel')

    npops = [args.npops // nc] * nc

    for i in xrange(args.npops % nc):
        npops[i] += 1

    for i in xrange(nc):
        rc[i].apply(parallel.init,
                    npops[i], args.n, args.popsize,
                    zero_diag=args.zero_diag)

    for i in xrange(args.generations):
        print("Generation %d" % i, file=sys.stderr)

        print_nets = True if i == args.generations - 1 else False

        dv.apply(parallel.tick,
                 mutation=args.mutation,
                 zero_diag=args.zero_diag,
                 print_nets=print_nets)

        dv.execute('stats = parallel.stats')
        stats = dv.gather('stats')

        print_tick(printer, stats)

if __name__ == '__main__':
    main()
