# # @cuda.jit
# # def my_kernel(io_array):
# #     # Thread id in a 1D block
# #     tx = cuda.threadIdx.x
# #     # Block id in a 1D grid
# #     ty = cuda.blockIdx.x
# #     # Block width, i.e. number of threads per block
# #     bw = cuda.blockDim.x
# #     # Compute flattened index inside the array
# #     pos = tx + ty * bw
# #     if pos < io_array.size:  # Check array boundaries
# #         io_array[pos] *= 2 # do the computation
#
# # from __future__ import division
# from numba import cuda, njit
# import numpy
# import math
# import time
#
# @cuda.jit(device=True)
# def mult(a, shape):
#     res = 0.0
#     y = cuda.grid(1)
#     if y < shape:
#         res += a[y] + 1
#     return res
#
# # CUDA kernel
# @cuda.jit
# def increment_a_2D_array(an_array):
#     x, y = cuda.grid(2)
#     if x < an_array.shape[0] and y < an_array.shape[1]:
#        an_array[x, y] = mult(an_array[x, :], an_array.shape[1])
#     # if x < an_array.shape[0] and y < an_array.shape[1]:
#     #    an_array[x, y] = True
#
#
# # Host code
# an_array = numpy.ones((256, 3))
# d_image = cuda.to_device(an_array)
# threadsperblock = (2, 2)
# blockspergrid_x = math.ceil(an_array.shape[0] / threadsperblock[0])
# blockspergrid_y = math.ceil(an_array.shape[1] / threadsperblock[1])
# blockspergrid = (blockspergrid_x, blockspergrid_y)
# start = time.time()
# increment_a_2D_array[blockspergrid, threadsperblock](d_image)
# print(time.time() - start)
# an_array = d_image.copy_to_host()
# print(an_array)
# # print(an_array[2, 2])


import cupy
import time
from threading import Thread

def gpu_stream(stream):
    for i in range(100):
        x = cupy.ones((1, 124))
        y = cupy.ones((124, 1))
        print(stream)
        z = cupy.matmul(x, y)
        z = cupy.matmul(x, y)
        z = cupy.matmul(x, y)
        z = cupy.matmul(x, y)
        z = cupy.matmul(x, y)
        z = cupy.matmul(x, y)
        z = cupy.matmul(x, y)

if __name__ == '__main__':

    device = cupy.cuda.Device()
    memory_pool = cupy.cuda.MemoryPool()
    cupy.cuda.set_allocator(memory_pool.malloc)
    rand = cupy.random.RandomState(seed=1)

    n = 10
    zs = []
    map_streams = []
    stop_events = []
    reduce_stream = cupy.cuda.stream.Stream()
    for i in range(n):
        map_streams.append(cupy.cuda.stream.Stream())

    start_time = time.time()

    processes = []
    for stream in map_streams:
        processes.append(Thread(target=gpu_stream, args=(stream, )))
        print(stream)

    # Map
    for i, stream in enumerate(map_streams):
        with stream:
            print(i)
            processes[i].start()

    for i in range(n):
        processes[i].join()

    print("ok")

    #         zs.append(z)
    #     stop_event = stream.record()
    #     stop_events.append(stop_event)
    #
    # # Block the `reduce_stream` until all events occur. This does not block host.
    # # This is not required when reduction is performed in the default (Stream.null)
    # # stream unless streams are created with `non_blocking=True` flag.
    # for i in range(n):
    #     reduce_stream.wait_event(stop_events[i])
    #
    # # Reduce
    # with reduce_stream:
    #     z = sum(zs)
    #
    # device.synchronize()
    # elapsed_time = time.time() - start_time
    # print('elapsed time', elapsed_time)
    # print('total bytes', memory_pool.total_bytes())
    #
    # # Free all blocks in the memory pool of streams
    # for stream in map_streams:
    #     memory_pool.free_all_blocks(stream=stream)
    # print('total bytes', memory_pool.total_bytes())