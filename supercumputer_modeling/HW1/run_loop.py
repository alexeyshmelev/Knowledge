import numpy as np
import os
import subprocess

files = sorted(os.listdir('arrays/arrays_c/'))
x = [500*i for i in range(1, 11)]
t = []
gf = []
for f in files:
    print('ok')
    with open('arrays/arrays_c/'+f) as fl:
        result = subprocess.run(["./a.out"], input='\n'.join([l for l in fl]), capture_output=True, text=True)
        t.append(float(result.stdout.split('\n')[0].split(' ')[1]))
        gf.append(float(result.stdout.split('\n')[2].split(' ')[1]))

np.savetxt('times.txt', np.array(t))
np.savetxt('gflops.txt', np.array(gf))