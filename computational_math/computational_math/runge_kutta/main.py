from numba import njit, cfunc, prange, jit
import numpy as np
from scipy.optimize import root, bisect
import matplotlib.pyplot as plt
from multiprocessing import Process, Array
import time

jkw = dict(cache=True)

A = np.array([[0,          0,           0,          0,          0,              0,     0],
             [1/5,        0,           0,          0,          0,              0,     0],
             [3/40,       9/40,        0,          0,          0,              0,     0],
             [44/45,      -56/15,      32/9,       0,          0,              0,     0],
             [19372/6561, -25360/2187, 64448/6561, -212/729,   0,              0,     0],
             [9017/3168,  -355/33,     46732/5247, 49/176,     -5103/18656,    0,     0],
             [35/384,     0,           500/1113,   125/192,    -2187/6784,     11/84, 0]])

c = np.array([0, 1/5, 3/10, 4/5, 8/9, 1, 1])

b = np.array([35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0])


@njit(**jkw)
def rk5_nsteps_planes(f, t, s, h, mc, n, pl):
    """
    Повторение алгоритма метода Рунге-Кутты для вычисления таблицы (независимый аргумент, вектор состояния)
    :param f: исходная система (crtbp_ode)
    :param t: вектор t (независимый агрумент)
    :param s: вектор s (вектор состояния)
    :param h: шаг по времени
    :param mc: параметры системы
    :param n: количество итераций
    :param pl: ограничение на плосоксти
    :return: решение (таблица)
    """
    arr = np.empty((n + 1, s.shape[0] + 1))
    arr[:, 0] = t + h * np.arange(n + 1)
    arr[0, 1:] = s

    i = 0
    for i in range(n):
        arr[i + 1, 1:] = rk5_step(f, arr[i, 0], arr[i, 1:], h, mc)
        x = arr[i + 1, 1]
        if x < pl[0] or x > pl[1]:
            break

    return arr[:i + 2]


@njit(**jkw)
def rk5_step(f, t, s, h, mc):
    """
    Каждый отдельный шаг метода Рунге-Кутты
    :param f: исходная система (crtbp_ode)
    :param t: вектор t (независимый агрумент)
    :param s: вектор s (вектор состояния)
    :param h: шаг по времени
    :param mc: параметры системы
    :return: результат одного шага методом Рунге-Кутты
    """

    ks = np.zeros((len(A), 6))

    for i in range(len(A)):
        tmp = np.zeros(6)
        for j in range(len(A)):
            tmp += A[i, j] * ks[j] * h
        ks[i, :] = f(t + h * c[i], s + tmp, mc)

    tmp = np.zeros(6)
    for i in range(len(A)):
        tmp += b[i] * ks[i] * h

    return s + tmp


@njit(**jkw)
def crtbp_ode(t, s, mc):
    """
    Исходная система
    :param t: вектор t (независимый агрумент)
    :param s: вектор s (вектор состояния)
    :param mc: параметры системы
    :return:
    """
    x, y, z, vx, vy, vz = s
    mu2 = mc[0]
    mu1 = 1. - mu2

    r1 = ((x + mu2)**2 + y**2 + z**2)**0.5
    r2 = ((x - mu1)**2 + y**2 + z**2)**0.5

    ax = 2*vy + x - (mu1 * (x + mu2)/r1**3 + mu2 * (x - mu1)/r2**3)
    c = (mu1 / r1**3 + mu2 / r2**3)
    ay = -2*vx + y - c * y
    az = -c * z

    return np.array([vx, vy, vz, ax, ay, az], dtype=np.float64)


def get_plane(vy, f, s, h, mc, n, pl):
    """
    В какой стороне находится осмический аппарат
    :param vy: точка (координата y), которая передаётся в функцию (scipy.optimize.bisect автоматически меняет эту точку)
    :param f: исходная система (crtbp_ode)
    :param s: вектор s (вектор состояния)
    :param h: шаг по времени
    :param mc: параметры системы
    :param n: количество итераций
    :param pl: ограничение на плосоксти
    :return: в какой стороне аппарат (но вообже это важно только для ого, чтобы bisect имела разные знаки на концах промежутка)
    """
    s0 = s.copy()
    s0[4] = vy
    arr = rk5_nsteps_planes(f, 0., s0, h, mc, n, pl)
    x = arr[-1, 1]
    xmean = np.mean(pl)
    return -1 if x < xmean else 1


def loop(N, get_plane, crtbp_ode, h, mc, pl, x_range, z_range, arr, i):
    """
    Распараллеливание по каждой строчке
    :param N: размер сетки
    :param get_plane: функция (с тем же названием)
    :param crtbp_ode: функция (с тем же названием)
    :param h: шаг по времени
    :param mc: параметры системы
    :param pl: ограничение на плосоксти
    :param x_range: разбиение сетки по x
    :param z_range: разбиение сетки по z
    :param arr: multiprocessing.Array (чтобы вернуть значениея из процесса)
    :param i: текущая строчка
    :return: None
    """

    for j in range(N):
        print(f'N={N}', i, j)
        s0 = np.zeros(6)
        s0[0] = x_range[i]
        s0[2] = z_range[j]
        arr[j] = bisect(get_plane, -0.1, 0.1, args=(crtbp_ode, s0, h, mc, 20000, pl), xtol=1e-16)


def GetHeatmap(N, R, xL1, get_plane, crtbp_ode, h, mc, pl):
    """
    Рассчёт цветовых карт
    :param N: размер сетки
    :param R: расстояние Солнце-Земля
    :param xL1: расположение спутника
    :param get_plane: функция (с тем же названием)
    :param crtbp_ode: функция (с тем же названием)
    :param h: шаг по времени
    :param mc: параметры системы
    :param pl: ограничение на плосоксти
    :return: матрицу цветовой карты, разбиение по x (в километрах), разбиение по z (в километрах)
    """

    x_range = np.linspace(xL1 - 1e6 / 2 / R, xL1 + 1e6 / 2 / R, N)
    z_range = np.linspace(0., 1e6 / R, N)
    grid = np.zeros((N, N))

    ps = []
    m_arr = []

    for i in range(N//2):
        arr = Array('d', range(N))

        p = Process(target=loop, args=(N, get_plane, crtbp_ode, h, mc, pl, x_range, z_range, arr, i))
        p.start()

        m_arr.append(arr)
        ps.append(p)

    for i, p in enumerate(ps):
        p.join()
        grid[i, :] = np.array(m_arr[i])

    # идёт разбиение на части, т.к. не получается работать с большим количеством процессов

    for i in range(N//2, N):
        arr = Array('d', range(N))

        p = Process(target=loop, args=(N, get_plane, crtbp_ode, h, mc, pl, x_range, z_range, arr, i))
        p.start()

        m_arr.append(arr)
        ps.append(p)

    for i, p in enumerate(ps):
        p.join()
        grid[i, :] = np.array(m_arr[i])

    return grid, (x_range - xL1) * R, z_range * R


def g(x, mc):
    """
    Вычисление позиции спутника
    :param x: начальная догадка
    :param mc: параметры системы
    :return: координата по x
    """
    s = np.zeros(6)
    s[0] = x
    return crtbp_ode(0, s, mc)[3]


def get_jacobi_matrix_element(v, x, z, m1, m2):
    """
    Вычисление матрицы Якоби
    :param v: скорость
    :param i: позиция по x
    :param j: позиция по y
    :param m1: константа
    :param m2: константа
    :return: константа j
    """
    r1 = ((x + m2) ** 2 + z**2) ** 0.5
    r2 = ((x - m1) ** 2 + z**2) ** 0.5
    u = 0.5 * x ** 2 + m1 / r1 + m2 / r2
    return 2*u - v**2


def plot(mtrx, type, sec, x_range, z_range):
    """
    Рисование тепловой карты
    :param grid: матрица тепловой карты
    :return: None
    """
    px = 1 / plt.rcParams['figure.dpi']
    plt.clf()
    fig, ax = plt.subplots(1, 1, figsize=(20000 * px, 20000 * px))

    x_label_list = np.round(x_range)
    y_label_list = np.round(z_range)
    ax.set_xticks([j for j in range(s)])
    ax.set_yticks([j for j in range(s)])
    ax.set_xticklabels(x_label_list, fontsize=5 * 320 / s, rotation=90)
    ax.set_yticklabels(y_label_list, fontsize=5 * 320 / s)

    ax.set_xlabel('X coordinate (km) (xL1 relatively)', fontsize=150)
    ax.set_ylabel('Z coordinate (km)', fontsize=150)

    plt.title(f'Case {s} x {s}, took {round(sec / 60, 1)} min', fontsize=300)

    img = ax.imshow(mtrx)
    cb = fig.colorbar(img)
    cb.ax.tick_params(labelsize=125)
    if type == 'g':
        plt.savefig(f'heatmap_{i}.png')
    if type == 'u':
        plt.savefig(f'jacobi_matrix_{i}.png')


if __name__ == '__main__':
    mu2 = 3.001348389698916e-06
    mu1 = 1 - mu2
    R = 149600000  # км, среднее расстояние Солнце-Земля

    x0 = 3/4 * mu1
    mc = np.array([mu2])

    xL1 = root(g, x0, mc, tol=1e-12).x[0]

    d = (mu1 - xL1) * 0.99
    xmin = xL1 - d
    xmax = xL1 + d
    h = 0.001721420632103996  # шаг по времени

    pl = np.array([xmin, xmax])

    sizes = [40, 80, 160, 320]
    mins = [204, 462, 1620, 5802]

    for i, s in enumerate(sizes):

        start = time.time()
        grid, x_range, z_range = GetHeatmap(s, R, xL1, get_plane, crtbp_ode, h, mc, pl)
        end = time.time()

        with open(f'case_{i}.npy', 'wb') as f:
            np.save(f, grid)

        plot(grid.T, 'g', end - start, x_range, z_range)

        U = np.zeros((s, s))

        start = time.time()
        for j, x in enumerate(x_range):
            for k, z in enumerate(z_range):
                U[j, k] = get_jacobi_matrix_element(grid[j, k], x/R+xL1, z/R, mu1, mu2)
        end = time.time()

        plot(U.T, 'u', end - start, x_range, z_range)

        with open(f'jacobi_matrix_{i}.npy', 'wb') as f:
            np.save(f, U)
