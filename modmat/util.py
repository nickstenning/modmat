from __future__ import division

from collections import defaultdict

import numpy as np

def histogram(list_of_lists, f=len):
    hist = defaultdict(lambda: 0)
    for item in list_of_lists:
        hist[f(item)] += 1
    return [hist[i] for i in xrange(max(hist.keys()) + 1)]

def truncate_or_pad(ary, n, pad=None):
    if len(ary) < n:
        return ary + [pad] * (n - len(ary))
    else:
        return ary[:n]

def hamming_distance(a, b):
    n = a.shape[0]
    hd = 0
    for i in xrange(n):
        for j in xrange(n):
            if a[i, j] != b[i, j]:
                hd += 1
    return hd / (n * n)

def mean_hamming(population):
    n = len(population)
    i = np.random.randint(n)
    ind = population[i]

    hd = sum(hamming_distance(ind, population[(i + j) % n]) for j in xrange(1, n))
    return hd / n
