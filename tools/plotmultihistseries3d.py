import os
import sys

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.mlab import griddata
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

    # From the first generation of the first population, work out what the
    # maximum bin value is.

    # Average data, point-by-point, over all populations
    mean_data = data.mean(axis=0)
    # After this axis 0 is generation, 1 is num sccs
    mean_data = np.swapaxes(mean_data, 0, 1)


    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # X axis: generation
    xi = np.arange(1, len(mean_data[0]) + 1)
    # Y axis: num sccs
    yi = np.arange(len(mean_data))

    X, Y = np.meshgrid(xi, yi)

    Z = np.log(mean_data)

    surf = ax.plot_surface(X, Y, Z,
                           rstride=50, cstride=20, cmap=cm.jet,
                           linewidth=0, antialiased=True)


    if os.isatty(sys.stdout.fileno()):
        plt.show()
    else:
        plt.savefig(sys.stdout, format='png')

if __name__ == '__main__':
    main()
