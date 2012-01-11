from __future__ import division

import numpy as np

cimport cython
cimport numpy as np

cdef extern from "math.h":
    double sqrt(double x)
    double pow(double base, double exp)

__all__ = ['init', 'tick']

DTYPE = np.double
ctypedef np.double_t DTYPE_t

ENTRY_DENSITY = 0.1

INIT_SIZE = 1.0
MUTATION_SIZE = INIT_SIZE / 10

class InvalidCrossoverError(Exception):
    pass

def init(n, popsize, zero_diag=False):
    population = [_random_matrix(n, zero_diag=zero_diag) for _ in xrange(popsize)]
    return population, _evaluate_fitnesses(population)

def tick(population, fitnesses, zero_diag=False, mutation=False):
    new_population = []
    for _ in xrange(len(population) // 2):
        new_population.extend(_get_children(population, fitnesses,
                                            zero_diag=zero_diag, mutation=mutation))

    new_population = new_population[:len(population)]
    return new_population, _evaluate_fitnesses(new_population)

def _random_matrix(n, zero_diag=False):
    ary = np.zeros((n, n))

    for i in xrange(n):
        for j in xrange(n):
            if not zero_diag or i != j:
                if np.random.rand() < ENTRY_DENSITY:
                    ary[i, j] = np.random.uniform(-INIT_SIZE, INIT_SIZE)

    return ary

_coerce_complex = np.vectorize(np.complex)

@cython.cdivision(True)
def _prop_negative_eigvals(np.ndarray[DTYPE_t, ndim=2] mat):
    cdef np.ndarray[np.complex_t, ndim=1] eigvals = _coerce_complex(np.linalg.eigvals(mat))
    cdef int n_eigvals = eigvals.shape[0]
    cdef double count = 0.0

    for i in xrange(n_eigvals):
        if eigvals[i].real < 0.0:
            count += 1

    return count / (1.0 * n_eigvals)

@cython.cdivision(True)
def _knockout_fitness(np.ndarray[DTYPE_t, ndim=2] mat):
    cdef np.ndarray[np.complex_t, ndim=1] eigvals = _coerce_complex(np.linalg.eigvals(mat))
    cdef int n_eigvals = eigvals.shape[0]

    # Knock out a random edge
    edges = zip(*mat.nonzero())
    edge = edges[np.random.randint(len(edges))]

    cdef np.ndarray[DTYPE_t, ndim=2] mat_new = mat.copy()
    mat_new[edge] = 0.0

    # Compute new e-values
    cdef np.ndarray[np.complex_t, ndim=1] eigvals_new = _coerce_complex(np.linalg.eigvals(mat_new))

    cdef double distance = 0.0
    cdef double rdelta
    cdef double idelta

    for i in xrange(n_eigvals):
        rdelta = eigvals[i].real - eigvals_new[i].real
        idelta = eigvals[i].imag - eigvals_new[i].imag
        distance += sqrt(rdelta * rdelta + idelta * idelta)

    distance = pow(distance, 1/(1.0 * n_eigvals))

    return 1 / (1.0 + distance)

def _evaluate_fitnesses(population):
    # return [_prop_negative_eigvals(mat) for mat in population]
    return [_knockout_fitness(mat) for mat in population]

def _roulette_select(population, fitnesses):
    tot = sum(fitnesses)
    pick = tot * np.random.rand()
    sofar = 0.0

    for i, mat in enumerate(population):
        sofar += fitnesses[i]
        if sofar > pick:
            return mat

    raise Exception("Shit's goin' down. How the hell did I get here?")

def _matrix_crossover(ma, mb):
    if ma.shape != mb.shape:
        raise InvalidCrossoverError("Can't crossover matrices: matrix shapes must be identical!")

    if ma.shape[0] != mb.shape[1]:
        raise InvalidCrossoverError("Can't crossover non-square matrices!")

    corner_1, corner_2 = np.random.randint(ma.shape[0] + 1, size=(2, 2))

    for i in xrange(2):
        if corner_1[i] > corner_2[i]:
            corner_1[i], corner_2[i] = corner_2[i], corner_1[i]

    copya = ma.copy()
    copyb = mb.copy()

    copya[corner_1[0]:corner_2[0],corner_1[1]:corner_2[1]] = mb[corner_1[0]:corner_2[0],corner_1[1]:corner_2[1]]
    copyb[corner_1[0]:corner_2[0],corner_1[1]:corner_2[1]] = ma[corner_1[0]:corner_2[0],corner_1[1]:corner_2[1]]

    return copya, copyb

# Modifies matrix in-place
def _matrix_mutate(m, zero_diag=False):
    n = m.shape[0]

    for i in xrange(n):
        for j in xrange(n):
            if not zero_diag or i != j:
                if np.random.rand() < 1 / (10 * n * n):
                    m[i, j] += np.random.uniform(-MUTATION_SIZE, MUTATION_SIZE)

def _get_children(population, fitnesses, zero_diag=False, mutation=False):
    a = _roulette_select(population, fitnesses)
    b = _roulette_select(population, fitnesses)

    ap, bp = _matrix_crossover(a, b)

    if mutation:
        _matrix_mutate(ap, zero_diag=zero_diag)
        _matrix_mutate(bp, zero_diag=zero_diag)

    return ap, bp




