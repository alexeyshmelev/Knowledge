import numpy as np
import os
import subprocess

files = sorted(os.listdir('/home/avshmelev/bash_scripts/sm/c++/'))
x = [600*i for i in range(1, 11)]
t = []
gf = []
for f in files:
    with open('/home/avshmelev/bash_scripts/sm'+f) as fl:
        result = subprocess.run(["./a.out"], input='\n'.join([l for l in fl]), capture_output=True, text=True)
        t.append(float(result.stdout.split('\n')[0].split(' ')[1]))
        gf.append(float(result.stdout.split('\n')[2].split(' ')[1]))

np.savetxt('times.txt', np.array(t))
np.savetxt('gflops.txt', np.array(gf))
