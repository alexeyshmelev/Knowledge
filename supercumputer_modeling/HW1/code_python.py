import numpy as np
from time import time
import os

steps = 6
path = '/home/avshmelev/bash_scripts/sm'
t, flops = [], []

files = sorted(os.listdir(path))
for f in files:
    arr = np.loadtxt(path+f)
    n = arr.shape[1]
    mforce = 0
    cforce = 0
    start = time()

    for k in range(steps):
        for i in range(n-1):
            for j in range(i+1, n):
                den = (arr[1, i] - arr[1, j])**2 + (arr[2, i] - arr[2, j])**2 + (arr[3, i] - arr[3, j])**2
                cforce = (arr[0, i] * arr[0, j]) / den
                if cforce > mforce:
                    mforce = cforce

    diff = time() - start
    t.append(diff / count_exper)
    flop.append(((n * (n - 1) / 2) * 10 * steps) / diff)
np.savetxt('times_py.txt', t)
np.savetxt('flops_py.txt', flops)
