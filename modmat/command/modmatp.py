from __future__ import absolute_import

import sys
from IPython.parallel import Client

from modmat import parallel
from modmat.printer import Printer
from modmat.command.modmat import parser

parser.add_argument('-i', '--iprofile',
                    help='IPython parallel profile to use', default='default')
parser.add_argument('-q', '--npops', type=int, default=8,
                    help='number of populations to simulate')

def main():
    args = parser.parse_args()

    printer = Printer(args.datadir, args.npops)

    rc = Client(profile=args.iprofile)
    nc = len(rc)

    dv = rc[:]
    dv.block = True

    print >>sys.stderr, "# Running on %s processes" % nc

    dv.execute('from modmat import parallel')

    npops = [args.npops // nc] * nc

    for i in xrange(args.npops % nc):
        npops[i] += 1

    for i in xrange(nc):
        rc[i].apply(parallel.init, npops[i], args.n, args.popsize)

    for _ in xrange(args.generations):
        dv.apply(parallel.tick)
        dv.execute('stats = parallel.stats')
        stats = dv.gather('stats')

        for i, s in enumerate(stats):
            printer.register(i, {
                'summary': "%10.4g %10.4g\n" % (s['mean_fit'], s['mean_sccs'])
            })

        printer.tick()

if __name__ == '__main__':
    main()
