#cython: language_level=3
cimport cython
cimport numpy as np
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def max_force(np.ndarray[double, ndim=1, mode="c"] m, np.ndarray[double, ndim=1, mode="c"] x, np.ndarray[double, ndim=1, mode="c"] y, np.ndarray[double, ndim=1, mode="c"] z):
    cdef:
        int n = m.shape[0]
        double max_force = 0.
        double cur_force = 0.
        int i 
        int j
        double den
    for i in range(n-1):
            for j in range(i+1, n):
                den = (x[i] - x[j])*(x[i] - x[j]) + (y[i] - y[j])*(y[i] - y[j]) + (z[i] - z[j])*(z[i] - z[j])
                cur_force = (m[i] * m[j]) / den
                if cur_force > max_force:
                    max_force = cur_force
    return max_force