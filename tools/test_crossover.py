import numpy as np

a = np.ones((10, 10))
b = np.zeros((10, 10))

choice_old = np.zeros((10, 10))
choice_new = np.zeros((10, 10))

def old_crossover(ma, mb):
    corner_1, corner_2 = np.random.randint(ma.shape[0] + 1, size=(2, 2))

    for i in xrange(2):
        if corner_1[i] > corner_2[i]:
            corner_1[i], corner_2[i] = corner_2[i], corner_1[i]

    for i in xrange(corner_1[0], corner_2[0]):
        for j in xrange(corner_1[1], corner_2[1]):
            choice_old[i, j] += 1

def new_crossover(ma, mb):
    n = ma.shape[0]

    corner = np.random.randint(n, size=2)
    szx, szy = np.random.randint(1, n + 1, size=2)

    for i in xrange(szx):
        for j in xrange(szy):
            choice_new[(corner[0] + i) % n, (corner[1] + j) % n] += 1

for i in xrange(1000):
    new_crossover(a, b)
    old_crossover(a, b)

print choice_old
print
print choice_new
