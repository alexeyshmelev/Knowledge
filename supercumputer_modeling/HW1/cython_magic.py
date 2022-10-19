from variant5_cython import max_force
import numpy as np
import os
from time import time
import timeit

count_exper = 1
tt = []
gf = []
mf = []

files = sorted(os.listdir('/home/avshmelev/bash_scripts/sm/python/'))
for f in files:
    arr = np.loadtxt('/home/avshmelev/bash_scripts/sm/python/'+f)
    n = arr.shape[1]

    t = time()
    for i in range(count_exper):
        max_force(arr[0], arr[1], arr[2], arr[3])
    t = time() - t
    mforce = max_force(arr[0], arr[1], arr[2], arr[3])

    tt.append(t / count_exper)
    gf.append(((n*(n-1)/2) * 13 * count_exper)  / t)
    mf.append(mforce)
np.savetxt('times_cython.txt', tt)
np.savetxt('gflops_cython.txt', gf)
np.savetxt('answers_cython.txt', mf)
