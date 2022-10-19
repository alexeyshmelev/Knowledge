from variant5_cython import max_force
import numpy as np
import os
from time import time
import timeit

count_exper = 1000
tt = []
gf = []
mf = []

files = sorted(os.listdir('arrays/arrays_py/'))
for f in files:
    arr = np.loadtxt('arrays/arrays_py/'+f)
    n = arr.shape[1]

    # t = timeit.timeit('max_force(arr[0], arr[1], arr[2], arr[3])', number=count_exper, globals=globals())
    t = time()
    for i in range(count_exper):
        max_force(arr[0], arr[1], arr[2], arr[3])
    t = time() - t
    mforce = max_force(arr[0], arr[1], arr[2], arr[3])

    print('Answer:', mforce)
    print('Timing:', t, 'seconds')
    print('Timing per run:', t / count_exper, 'seconds')
    print('GFlops:', ((n*(n-1)/2) * 13 * count_exper)  / (t*1e9))
    tt.append(t / count_exper)
    gf.append(((n*(n-1)/2) * 13 * count_exper)  / t)
    mf.append(mforce)
np.savetxt('times_cython.txt', tt)
np.savetxt('gflops_cython.txt', gf)
np.savetxt('answers_cython.txt', mf)
