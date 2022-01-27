import numpy as np
from scipy.spatial.distance import cdist
from numba import njit, prange, cuda, jit
import math
import cupy as cp

memory_pool = cp.cuda.MemoryPool()
cp.cuda.set_allocator(memory_pool.malloc)

@cuda.jit(device=True)
def mean_axis0_gpu(arr, res):
    n = arr.shape[1]
    res = np.empty(n, dtype=arr.dtype)
    for i in range(n):
        res[i] = arr[:, i].mean()
    return res


@cuda.jit
def new_simulate(boids, D, M, perception, asp, coeffs, left, right, bottom, top, ax, ay, wa):
    # M, left, right, bottom, top, ax, ay, wa, accels, res - zeros matrix
    # calc_dist
    arr = boids[:, :2]
    n = arr.shape[0]
    i, j = cuda.grid(2)
    if i < n and j < n and i < j:
        d = ((arr[j, 0] - arr[i, 0]) ** 2 + (arr[j, 1] - arr[i, 1]) ** 2) ** 0.5
        D[i, j] = d
        D[j, i] = d
    # check radius
    if i < n and j < n and i != j:
        if D[i, j] < perception:
            M[i, i] = 1.
    # wall avoidance
    if i < n:
        left[i] = math.fabs(boids[i, 0])
        right[i] = math.fabs(asp - boids[i, 0])
        bottom[i] = math.fabs(boids[i, 1])
        top[i] = math.fabs(1 - boids[i, 1])

        ax[i] = 1 / left[i] ** 2 - 1 / right[i] ** 2
        ay[i] = 1 / bottom[i] ** 2 - 1 / top[i] ** 2

        wa[i, 0] = ax[i]
        wa[i, 1] = ay[i]


def simulate_cpu(boids, D, M, wa, coeffs):
    boids = cp.asarray(boids)
    D = cp.asarray(D)
    M = cp.asarray(M)
    wa = cp.asarray(wa)
    coeffs = cp.asarray(coeffs)

    device = cp.cuda.Device()
    global memory_pool

    map_streams = []
    stop_events = []
    reduce_stream = cp.cuda.stream.Stream()
    for i in range(M.shape[0]):
        map_streams.append(cp.cuda.stream.Stream())

    for i, stream in enumerate(map_streams):
        with stream:
            idx = cp.where(M[i])[0]  # в каких местах True
            accels = cp.zeros((5, 2))
            if idx.size > 0:
                accels[0] = alignment(boids, i, idx)
                accels[1] = cohesion(boids, i, idx)
                accels[2] = separation(boids, i, idx, D)
            accels[3] = wa[i]
            # clip_mag(accels, *arange)
            boids[i, 4:6] = cp.sum(accels * coeffs.reshape(-1, 1), axis=0)
        stop_event = stream.record()
        stop_events.append(stop_event)

    for i in range(M.shape[0]):
        reduce_stream.wait_event(stop_events[i])

    with reduce_stream:
        boids = boids.get()
        D = D.get()
        M = M.get()
        wa = wa.get()
        coeffs = coeffs.get()
    device.synchronize()

    for stream in map_streams:
        memory_pool.free_all_blocks(stream=stream)

    # for i in range(boids.shape[0]):
    #     idx = np.where(M[i])[0] # в каких местах True
    #     accels = np.zeros((5, 2))
    #     if idx.size > 0:
    #         accels[0] = alignment(boids, i, idx)
    #         accels[1] = cohesion(boids, i, idx)
    #         accels[2] = separation(boids, i, idx, D)
    #     accels[3] = wa[i]
    #     # clip_mag(accels, *arange)
    #     boids[i, 4:6] = np.sum(accels * coeffs.reshape(-1, 1), axis=0)





def simulate(boids, D, perception, asp, coeffs):
    threadsperblock = (32, 32)
    blockspergrid_x = math.ceil(D.shape[0] / threadsperblock[0])
    blockspergrid_y = math.ceil(D.shape[1] / threadsperblock[1])
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    # data = np.copy(boids[:, :2])

    calc_dist[blockspergrid, threadsperblock](boids, D)

    # boids[:, :2] = data
    M = D < perception
    np.fill_diagonal(M, False)
    wa = wall_avoidance(boids, asp)
    for i in range(boids.shape[0]):
        idx = np.where(M[i])[0] # в каких местах True
        accels = np.zeros((5, 2))
        if idx.size > 0:
            accels[0] = alignment(boids, i, idx)
            accels[1] = cohesion(boids, i, idx)
            accels[2] = separation(boids, i, idx, D)
        accels[3] = wa[i]
        # clip_mag(accels, *arange)
        boids[i, 4:6] = np.sum(accels * coeffs.reshape(-1, 1), axis=0)



def mean_axis0(arr):
    n = arr.shape[1]
    res = cp.empty(n, dtype=arr.dtype)
    for i in range(n):
        res[i] = arr[:, i].mean()
    return res


@njit
def clip_mag(arr, low, high):
    mag = np.sum(arr * arr, axis=1) ** 0.5
    mask = mag > 1e-16
    mag_cl = np.clip(mag[mask], low, high)
    arr[mask] *= (mag_cl / mag[mask]).reshape(-1, 1)


@njit(cache=True)
def init_boids(boids, asp, vrange=(0., 1.), seed=0):
    N = boids.shape[0]
    np.random.seed(seed)
    boids[:, 0] = np.random.rand(N) * asp
    boids[:, 1] = np.random.rand(N)
    v = np.random.rand(N) * (vrange[1] - vrange[0]) + vrange[0]
    alpha = np.random.rand(N) * 2 * np.pi
    c, s = np.cos(alpha), np.sin(alpha)
    boids[:, 2] = v * c
    boids[:, 3] = v * s


@njit(cache=True)
def directions(boids):
    return np.hstack((boids[:, :2] - boids[:, 2:4], boids[:, :2]))


@njit(cache=True)
def propagate(boids, dt, vrange):
    boids[:, :2] += dt * boids[:, 2:4] + 0.5 * dt ** 2 * boids[:, 4:6]
    boids[:, 2:4] += dt * boids[:, 4:6]
    clip_mag(boids[:, 2:4], vrange[0], vrange[1])


@cuda.jit
def calc_dist(arr, D): # вычисление расстояний между всеми boids
    data = arr[:, :2]
    n = data.shape[0]
    i, j = cuda.grid(2)
    if i < n and j < n and i < j:
        d = ((data[j, 0]-data[i, 0])**2 + (data[j, 1]-data[i, 1])**2)**0.5
        D[i, j] = d
        D[j, i] = d

    # n = arr.shape[0]
    # for i in prange(n):
    #     for j in range(i):
    #         v = arr[j] - arr[i]
    #         d = (v @ v) ** 0.5
    #         D[i, j] = d
    #         D[j, i] = d


# @njit(cache=True)
# def calc_neighbors(boids, D, perception):
#     N = boids.shape[0]
#
#     # mask[range(N), range(N)] = False
#     return mask, D

@njit(cache=True)
def periodic_walls(boids, asp):
    boids[:, :2] %= np.array([asp, 1.])


def alignment(boids, i, idx):
    avg = mean_axis0(boids[idx, 2:4])
    a = avg - boids[i, 2:4]
    return a



def cohesion(boids, i, idx):
    center = mean_axis0(boids[idx, 0:2])
    a = center - boids[i, 0:2]
    return a



def separation(boids, i, idx, D):
    d = boids[i, 0:2] - boids[idx, 0:2]
    a = cp.sum(d / D[i][idx].reshape(-1, 1), axis=0)
    return a


@njit
def wall_avoidance(boids, asp):
    left = np.abs(boids[:, 0])
    right = np.abs(asp - boids[:, 0])
    bottom = np.abs(boids[:, 1])
    top = np.abs(1 - boids[:, 1])

    ax = 1 / left ** 2 - 1 / right ** 2
    ay = 1 / bottom ** 2 - 1 / top ** 2

    return np.column_stack((ax, ay))