import numpy as np
from scipy.spatial.distance import cdist
from numba import njit, cuda, jit
import math
import time


@cuda.jit
def new_simulate(boids, D, perception, asp, coeffs, left, right, bottom, top, wa, accels, tmp, counter, counter2d):
    """
    Производит основную часть симуляции на GPU (все использованные переменные мы передаём заранее, т.к. прямым образом выделить новую память на GPU нельзя)

    :param boids: массив, содержащий всю необходимую информацию о каждом boid
    :param D: матрица расстояний
    :param perception: радиус восприятия для каждого boid
    :param asp: соотношение сторон
    :param coeffs: коэффициенты для каждого тыпа ускорений
    :param left: массив для хранения данных, учитывающихся при отталкивании от левой границы
    :param right: массив для хранения данных, учитывающихся при отталкивании от правой границы
    :param bottom: массив для хранения данных, учитывающихся при отталкивании от нижней границы
    :param top: массив для хранения данных, учитывающихся при отталкивании от верхней границы
    :param wa: изменения ускорений при отталкивании от границы
    :param accels: массив со всеми ускорениями для каждого boid
    :param tmp: массив для хранения промежуточных вычислений
    :param counter: массив для хранения промеруточных вычислений
    :param counter2d: массив для хранения промеруточных вычислений
    :return: boids с именёнными параметрами ускорений как ссылку
    """
    n = boids.shape[0]
    i, j = cuda.grid(2)

    # pairwise distance matrix
    if n > i != j < n:
        D[i, j] = ((boids[j, 0] - boids[i, 0]) ** 2 + (boids[j, 1] - boids[i, 1]) ** 2) ** 0.5

    cuda.syncthreads()

    # wall avoidance
    if i < n and j == 0:
        left[i] = math.fabs(boids[i, 0])
        right[i] = math.fabs(asp - boids[i, 0])
        bottom[i] = math.fabs(boids[i, 1])
        top[i] = math.fabs(1 - boids[i, 1])

        wa[i, 0] = 1 / left[i] ** 2 - 1 / right[i] ** 2
        wa[i, 1] = 1 / bottom[i] ** 2 - 1 / top[i] ** 2
        accels[i, :, :] = 0

    cuda.syncthreads()

    if i < n and j < n:
        tmp[i, j, :] = 0

    cuda.syncthreads()

    # alignment
    mean_gpu(boids, D, i, j, n, 2, 3, accels, counter, counter2d, perception)
    cuda.syncthreads()
    # # cohesion
    mean_gpu(boids, D, i, j, n, 0, 1, accels, counter, counter2d, perception)
    cuda.syncthreads()
    # separation
    separation_gpu(boids, D, i, j, n, accels, perception, counter2d, tmp)
    cuda.syncthreads()

    if i < n and j == 0:
        accels[i, 3, 0] = wa[i, 0]
        accels[i, 3, 1] = wa[i, 1]
        accels[i, 4, 0] = asp / 2 - boids[i, 0]
        accels[i, 4, 1] = 1 / 2 - boids[i, 1]
        boids[i, 4] = accels[i, 0, 0] * coeffs[0] + accels[i, 1, 0] * coeffs[1] + accels[i, 2, 0] * coeffs[2] + accels[i, 3, 0] * coeffs[3] + accels[i, 4, 0] * coeffs[4]
        boids[i, 5] = accels[i, 0, 1] * coeffs[0] + accels[i, 1, 1] * coeffs[1] + accels[i, 2, 1] * coeffs[2] + accels[i, 3, 1] * coeffs[3] + accels[i, 4, 1] * coeffs[4]

    cuda.syncthreads()


@cuda.jit
def mean_gpu(boids, D, i, j, n, a, b, accels, counter, counter2d, perception):
    """
    Вычисление среднего значение по всем скоростям или ускорениям для каждой координаты для тех boid, которые находятся в радиусе perception

    :param boids: массив, содержащий всю необходимую информацию о каждом boid
    :param D: матрица расстояний
    :param i: поток по одному направлению в сетке
    :param j: поток по другому направлению в сетке
    :param n: количество boids
    :param a: скорость или ускорение по x
    :param b: скорость или ускорение по y
    :param accels: массив со всеми ускорениями для каждого boid
    :param counter: массив для хранения промеруточных вычислений
    :param counter2d: массив для хранения промеруточных вычислений
    :param perception: радиус восприятия для каждого boid
    :return: всё изменяется по ссылке
    """
    if i < n and j == 0:
        counter2d[i, 0] = 0
        counter2d[i, 1] = 0
        counter[i] = 0

    cuda.syncthreads()

    if i < n and j == 0:
        for k in range(n): # т.к. atomic operations работают с двумерной сеткой потоков неправильно, они блокируют только либо для i либо для j
            if 0 < D[k, i] < perception:
                cuda.atomic.add(counter2d, (i, 0), boids[k, a])
                cuda.atomic.add(counter2d, (i, 1), boids[k, b])
                cuda.atomic.add(counter, i, 1)

    if i < n and j == 0:
        if counter[i] != 0:
            counter2d[i, 0] /= counter[i]
            counter2d[i, 1] /= counter[i]
            if a == 2 and b == 3:
                accels[i, 0, 0] = math.sin(counter2d[i, 0] - boids[i, a])
                accels[i, 0, 1] = math.sin(counter2d[i, 1] - boids[i, b])
            if a == 0 and b == 1:
                accels[i, 1, 0] = counter2d[i, 0] - boids[i, a] ** 3
                accels[i, 1, 1] = counter2d[i, 1] - boids[i, b] ** 3


@cuda.jit
def separation_gpu(boids, D, i, j, n, accels, perception, counter2d, tmp):
    """
    Подсчёт составляющей ускорения, которая отвечает за рассредоточение boids

    :param boids: массив, содержащий всю необходимую информацию о каждом boid
    :param D: матрица расстояний
    :param i: поток по одному направлению в сетке
    :param j: поток по другому направлению в сетке
    :param n: количество boids
    :param accels: массив со всеми ускорениями для каждого boid
    :param perception: радиус восприятия для каждого boid
    :param counter2d: массив для хранения промеруточных вычислений
    :param tmp: массив для хранения промеруточных вычислений
    :return: всё изменяется по ссылке
    """
    if n > i != j < n:
        if 0 < D[i, j] < perception:
            tmp[i, j, 0] = (- math.sin(boids[j, 0]) + math.sin(boids[i, 0])) / D[i, j]
            tmp[i, j, 1] = (- math.sin(boids[j, 1]) + math.sin(boids[i, 1])) / D[i, j]

    cuda.syncthreads()

    if i < n and j == 0:
        for k in range(n):
            cuda.atomic.add(accels, (i, 2, 0), tmp[i, k, 0])
            cuda.atomic.add(accels, (i, 2, 1), tmp[i, k, 1])


@njit(cache=True)
def clip_mag(arr, low, high):
    """
    Ограничение скорости

    :param arr: массив для всех boids
    :param low: минимальная скорость
    :param high: максимальная скорость
    :return: всё изменяется по ссылке
    """
    mag = np.sum(arr * arr, axis=1) ** 0.5
    mask = mag > 1e-16
    mag_cl = np.clip(mag[mask], low, high)
    arr[mask] *= (mag_cl / mag[mask]).reshape(-1, 1)


@njit(cache=True)
def init_boids(boids, asp, vrange=(0., 1.), seed=0):
    """

    :param boids: массив для всех boids
    :param asp: соотношение сторон
    :param vrange: диапазон начальных скоростей
    :param seed: seed
    :return: всё изменяется по ссылке
    """
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
    """
    Рисование стрелок

    :param boids: массив для всех boids
    :return: всё изменяется по ссылке
    """
    return np.hstack((boids[:, :2] - boids[:, 2:4], boids[:, :2]))


@njit(cache=True)
def propagate(boids, dt, vrange):
    """
    Изменение скорости во времение

    :param boids: массив для всех boids
    :param dt: временной шаг
    :param vrange: диапазон начальных скоростей
    :return: всё изменяется по ссылке
    """
    boids[:, :2] += dt * boids[:, 2:4] + 0.5 * dt ** 2 * boids[:, 4:6]
    boids[:, 2:4] += dt * boids[:, 4:6]
    clip_mag(boids[:, 2:4], vrange[0], vrange[1])


@njit(cache=True)
def periodic_walls(boids, asp):
    """
    Обработка вылета за стену

    :param boids: массив для всех boids
    :param asp: соотношение сторон
    :return: всё изменяется по ссылке
    """
    boids[:, :2] %= np.array([asp, 1.])