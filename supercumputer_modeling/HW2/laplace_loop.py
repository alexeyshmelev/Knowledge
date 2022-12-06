import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt

flops = []

for i in range(1, 33):
    print(i)
    os.environ["OMP_NUM_THREADS"] = str(i)
    res = subprocess.run(["./a.out"], input='300\n', capture_output=True, text=True, shell=True)
    flops.append(float(res.stdout.split('\n')[-1].split(' ')[-1]))

plt.clf()
plt.plot(flops)
plt.title('FLOPS')
plt.ylabel('GFlops')
plt.xlabel('num_thread')
plt.savefig('laplace_flops.png')