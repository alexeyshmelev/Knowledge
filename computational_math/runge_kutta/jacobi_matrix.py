# import numpy as np
# from scipy.optimize import root
#
# def g(x, mc):
#     """
#     Вычисление позиции спутника
#     :param x: начальная догадка
#     :param mc: параметры системы
#     :return: координата по x
#     """
#     s = np.zeros(6)
#     s[0] = x
#     return crtbp_ode(0, s, mc)[3]
#
# mu2 = 3.001348389698916e-06
# mu1 = 1 - mu2
# R = 149600000  # км, среднее расстояние Солнце-Земля
#
# x0 = 3/4 * mu1
# mc = np.array([mu2])
#
# xL1 = root(g, x0, mc, tol=1e-12).x[0]
#
# x_range = np.linspace(xL1 - 1e6 / 2 / R, xL1 + 1e6 / 2 / R, N)
# z_range = np.linspace(0., 1e6 / R, N)
#
# def get_jacobi_matrix_element(v, i, j, m1, m2):
#     r1 = ((x_range[i, j] + m2) ** 2 + z_range[i, j]) ** 0.5
#     r2 = ((x_range[i, j] - m1) ** 2 + z_range[i, j]) ** 0.5
#     u = 0.5 * x_range[i, j] ** 2 + m1 / r1 + m2 / r2
#
#
# for i in range(4):

import numpy as np
import matplotlib.pyplot as plt

grid = np.load('case_3.npy')

px = 1 / plt.rcParams['figure.dpi']
plt.clf()
fig, ax = plt.subplots(1, 1, figsize=(8000 * px, 8000 * px))

x_label_list = np.round(x_range)
y_label_list = np.round(z_range)
ax.set_xticks([j for j in range(s)])
ax.set_yticks([j for j in range(s)])
ax.set_xticklabels(x_label_list, fontsize=4*320/s, rotation=90)
ax.set_yticklabels(y_label_list, fontsize=4*320/s)

ax.set_xlabel('X coordinate (km) (xL1 relatively)', fontsize=40)
ax.set_ylabel('Z coordinate (km)', fontsize=40)

plt.title(f'Case {s} x {s}, took {round((end - start) / 60, 1)} min', fontsize=50)