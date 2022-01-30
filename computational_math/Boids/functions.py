import numpy as np
from scipy.spatial.distance import cdist
from numba import njit, prange, cuda, jit
import math
import time



@cuda.jit
def new_simulate(boids, D, M, perception, asp, coeffs, left, right, bottom, top, ax, ay, wa, accels, tmp, counter, counter2d):
    # M, left, right, bottom, top, ax, ay, wa, accels, res - zeros matrix
    # calc_dist
    arr = boids[:, :2]
    n = arr.shape[0]
    i = cuda.grid(1)
    if i < n:
        for j in range(i):
            counter[i] = ((arr[j, 0] - arr[i, 0]) ** 2 + (arr[j, 1] - arr[i, 1]) ** 2) ** 0.5
            D[i, j] = counter[i]
            D[j, i] = counter[i]
    # check radius
    M[:, :] = 0.
    if i < n:
        for j in range(n):
            if D[i, j] < perception:
                if i != j:
                    M[i, j] = 1.
    # wall avoidance
    if i < n:
        left[i] = math.fabs(boids[i, 0])
        right[i] = math.fabs(asp - boids[i, 0])
        bottom[i] = math.fabs(boids[i, 1])
        top[i] = math.fabs(1 - boids[i, 1])

        wa[i, 0] = 1 / left[i] ** 2 - 1 / right[i] ** 2
        wa[i, 1] = 1 / bottom[i] ** 2 - 1 / top[i] ** 2
    # range
    accels[:, :, :] = 0
    tmp[:, :, :] = 0
    if i < n:
        # alignment
        mean_gpu(boids, M, i, n, 2, 3, accels, counter, counter2d)
        # cohesion
        mean_gpu(boids, M, i, n, 0, 1, accels, counter, counter2d)
        # separation
        separation_gpu(boids, M, i, n, tmp, D, accels, counter2d)

        accels[i, 3, 0] = wa[i, 0]
        accels[i, 3, 1] = wa[i, 1]

        boids[i, 4] = accels[i, 0, 0] * coeffs[0] + accels[i, 1, 0] * coeffs[1] + accels[i, 2, 0] * coeffs[2] + accels[i, 3, 0] * coeffs[3] + accels[i, 4, 0] * coeffs[4]
        boids[i, 5] = accels[i, 0, 1] * coeffs[0] + accels[i, 1, 1] * coeffs[1] + accels[i, 2, 1] * coeffs[2] + accels[i, 3, 1] * coeffs[3] + accels[i, 4, 1] * coeffs[4]


@cuda.jit(device=True)
def mean_gpu(boids, M, i, n, a, b, accels, counter, counter2d):
    counter2d[i, 0] = 0
    counter2d[i, 1] = 0
    counter[i] = 0
    for j in prange(n):
        if M[i, j] == 1:
            counter2d[i, 0] += boids[j, a]
            counter2d[i, 1] += boids[j, b]
            counter[i] += 1
    counter2d[i, 0] /= counter[i]
    counter2d[i, 1] /= counter[i]
    if a == 2 and b == 3:
        accels[i, 0, 0] = counter2d[i, 0] - boids[i, a]
        accels[i, 0, 1] = counter2d[i, 1] - boids[i, b]
    else:
        accels[i, 1, 0] = counter2d[i, 0] - boids[i, 0]
        accels[i, 1, 1] = counter2d[i, 1] - boids[i, 1]


@cuda.jit(device=True)
def separation_gpu(boids, M, i, n, tmp, D, accels, counter2d):
    counter2d[i, 0] = 0
    counter2d[i, 1] = 0
    for j in prange(n):
        if M[i, j] == 1:
            tmp[i, j, 0] = - boids[j, 0] + boids[i, 0]
            tmp[i, j, 1] = - boids[j, 1] + boids[i, 1]
            counter2d[i, 0] += tmp[i, j, 0] / D[i, j]
            counter2d[i, 1] += tmp[i, j, 1] / D[i, j]
    # for j in prange(n):
    #     if M[i, j] == 1:
    #         counter2d[i, 0] += tmp[i, j, 0] / D[i, j]
    #         counter2d[i, 1] += tmp[i, j, 1] / D[i, j]

    accels[i, 2, 0], accels[i, 2, 1] = counter2d[i, 0], counter2d[i, 1]


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


@njit(cache=True)
def periodic_walls(boids, asp):
    boids[:, :2] %= np.array([asp, 1.])