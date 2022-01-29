from __future__ import print_function

import sys

import numpy as np

from numba import guvectorize, cuda

if sys.version_info[0] == 2:
    range = xrange


#    function type:
#        - has void return type
#
#    signature: (n)->(n)
#        - the function takes an array of n-element and output same.

@guvectorize(['void(float32[:], float32[:])'], '(n) ->(n)', target='cuda')
def my_func(inp, out):
        tmp1 = 0.
        tmp = inp[0]
        for i in range(out.shape[0]):
            tmp1 += tmp
            out[i] = tmp1
            tmp *= inp[0]

# set up input data
rows = 1280000 # shape[0]
cols = 4   # shape[1]
inp = np.zeros(rows*cols, dtype=np.float32).reshape(rows, cols)
for i in range(inp.shape[0]):
    inp[i,0] = (i%4)+1
# invoke on CUDA with manually managed memory

dev_inp = cuda.to_device(inp)             # alloc and copy input data

my_func(dev_inp, dev_inp)             # invoke the gufunc

dev_inp.copy_to_host(inp)                 # retrieve the result

# print out
print('result'.center(80, '-'))
print(inp)