import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt

flops = []

for i in range(1, 33):
    os.environ["OMP_NUM_THREADS"] = str(i)
    arr_size = '220' #str(300 + 15 * (i-1)) if i <= 10 else '500'
    res = subprocess.run(["./a.out"], input=f"{arr_size}\n", capture_output=True, text=True, shell=True)
    n = float(res.stdout.split('\n')[-1].split(' ')[-1])
    t = res.stdout.split('\n')[0].split(' ')[1]
    print(f'num_threads: {i}, arr_size: {arr_size}, FLOPS: {n}, time: {t} sec')
    flops.append(n)

plt.clf()
plt.plot(flops)
plt.title('FLOPS')
plt.ylabel('GFlops')
plt.xlabel('num_thread')
plt.savefig('laplace_flops.png')
