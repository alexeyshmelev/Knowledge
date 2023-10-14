from numba import njit, cfunc, prange, jit
import numpy as np
from scipy.optimize import root, bisect
import matplotlib.pyplot as plt
from multiprocessing import Process, Array
import types

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
def rk5_nsteps_planes(t, s, h, mc, n, pl):
    arr = np.empty((n + 1, s.shape[0] + 1))
    arr[:, 0] = t + h * np.arange(n + 1)
    arr[0, 1:] = s

    i = 0
    for i in range(n):
        arr[i + 1, 1:] = rk5_step(arr[i, 0], arr[i, 1:], h, mc)
        x = arr[i + 1, 1]
        if x < pl[0] or x > pl[1]:
            break

    return arr[:i + 2]


@njit(**jkw)
def rk5_step(t, s, h, mc):

    ks = np.zeros((len(A), 6))

    for i in range(len(A)):
        tmp = np.zeros(6)
        for j in range(len(A)):
            tmp += A[i, j] * ks[j] * h
        ks[i, :] = crtbp_ode(t + h * c[i], s + tmp, mc)

    tmp = np.zeros(6)
    for i in range(len(A)):
        tmp += b[i] * ks[i] * h

    return s + tmp


# @cfunc('f8[:](f8, f8[:], f8[:])', **jkw)
@njit(**jkw)
def crtbp_ode(t, s, mc):
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


def get_plane(vy, s, h, mc, n, pl):
    s0 = s.copy()
    s0[4] = vy
    arr = rk5_nsteps_planes(0., s0, h, mc, n, pl)
    x = arr[-1, 1]
    xmean = np.mean(pl)
    return -1 if x < xmean else 1


# def InitV(get_plane, crtbp_ode, s0, h, mc, pl):
#     return bisect(get_plane, -0.1, 0.1, args=(crtbp_ode, s0, h, mc, 20000, pl), xtol=1e-16)

def compile_specialized_bisect(f):

    def python_bisect(a, b, xtol, args):

        its = 0
        fa = jit_root_func(a, *args)
        fb = jit_root_func(b, *args)

        if abs(fa) < xtol:
            return a
        elif abs(fb) < xtol:
            return b


        c = (a+b)/2.
        fc = jit_root_func(c, *args)

        while abs(fc)>xtol:

            its = its + 1

            if fa*fc < 0:
                b = c
                fb = fc

            else:
                a = c
                fa = fc

            c = (a+b)/2.
            fc = jit_root_func(c, *args)

        return c

    jit_root_func = jit(nopython=True)(get_plane)
    return jit(nopython=True)(python_bisect)


def numba_bisect(a, b, xtol, args):

    jit_bisect_root_func = compile_specialized_bisect(get_plane)
    return jit_bisect_root_func(a, b, xtol, args)


def loop(N, get_plane, crtbp_ode, h, mc, pl, x_range, z_range, arr, i):

    for j in range(N):
        print(i, j)
        s0 = np.zeros(6)
        s0[0] = x_range[i]
        s0[2] = z_range[j]
        arr[j] = numba_bisect(-0.1, 0.1, args=(s0, h, mc, 20000, pl), xtol=1e-16)


@njit(parallel=True)
def PlotHeatmap(N, R, xL1, get_plane, crtbp_ode, h, mc, pl):

    x_range = np.linspace(xL1 - 1e6 / 2 / R, xL1 + 1e6 / 2 / R, N)
    z_range = np.linspace(0., 1e6 / R, N)
    grid = np.zeros((N, N))

    for i in prange(N):
        for j in range(N):
            print(i, j)
            s0 = np.zeros(6)
            s0[0] = x_range[i]
            s0[2] = z_range[j]
            grid[i, j] = numba_bisect(-0.1, 0.1, args=(s0, h, mc, 20000, pl), xtol=1e-16)

    # ps = []
    # m_arr = []

    # for i in range(N):
    #     arr = Array('d', range(N))
    #
    #     p = Process(target=loop, args=(N, get_plane, crtbp_ode, h, mc, pl, x_range, z_range, arr, i))
    #     p.start()
    #
    #     m_arr.append(arr)
    #     ps.append(p)
    #
    # for i, p in enumerate(ps):
    #     p.join()
    #     grid[i, :] = np.array(m_arr[i])

    print(grid)

    return grid


def g(x, mc):
    s = np.zeros(6)
    s[0] = x
    return crtbp_ode(0, s, mc)[3]


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
    h = 0.001721420632103996  # nd, одни сутки, шаг по времени

    pl = np.array([xmin, xmax])

    s0 = np.zeros(6)
    s0[[0, 2, 4]] = xL1 + d * 0.1, d * 0.1, 0.02

    arr0 = rk5_nsteps_planes(0., s0, h, mc, 500, pl)

    s0 = np.zeros(6)
    s0[[0, 2, 4]] = xL1 + d * 0.1, d * 0.1, -0.02

    arr1 = rk5_nsteps_planes(0., s0, h, mc, 500, pl)

    # График на плоскости XOY

    plt.figure(dpi=200)

    # траектории
    plt.plot(arr0[:, 1], arr0[:, 2], label='$\dot{y}_0 > \dot{y}^*$')
    plt.plot(arr1[:, 1], arr1[:, 2], label='$\dot{y}_0 < \dot{y}^*$')

    # точка L1
    plt.plot(xL1, 0., 'ok')
    plt.text(xL1, 0., ' $L_1$')

    # Земля
    plt.plot(mu1, 0., 'ok')
    plt.text(mu1, 0., ' Earth')

    # Плоскости
    plt.axvline(xmin, ls='--', color='gray', alpha=0.5)
    plt.axvline(xmax, ls='--', color='gray', alpha=0.5)

    # Ось OX
    plt.axhline(0., ls='--', color='gray', alpha=0.5)

    plt.legend()

    plt.xlabel('x, nd')
    plt.ylabel('y, nd')

    # plt.show()

    ###############################################

    grid = PlotHeatmap(5, R, xL1, get_plane, crtbp_ode, h, mc, pl)
    plt.clf()
    plt.imshow(grid)
    plt.show()