from code_cythone import max_force
import numpy as np
import os
from time import time
import timeit

counter = 1000
tt = []
gf = []
mf = []

files = sorted(os.listdir('/home/avshmelev/bash_scripts/sm/python/'))
for f in files:
    arr = np.loadtxt('/home/avshmelev/bash_scripts/sm/python/'+f)
    n = arr.shape[1]

    t = time()
    for i in range(counter):
        max_force(arr[0], arr[1], arr[2], arr[3])
    t = time() - t
    mforce = max_force(arr[0], arr[1], arr[2], arr[3])

    tt.append(t / counter)
    gf.append(((n*(n-1)/2) * 13 * counter)  / t)
    mf.append(mforce)
np.savetxt('times_cython.txt', tt)
np.savetxt('gflops_cython.txt', gf)
np.savetxt('answers_cython.txt', mf)
