import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import spiceypy as spice
from utils import (load_kernels_from_path, merge_intervals,
                   window2df, split_by_max_duration, intersect_windows)

#%%
load_kernels_from_path(path='kernels')

#%% Задание
# Рассчитать интервалы видимости Луна-Глоб:
# - диапазон дат - из примера 3
# - с наземного пункта Медвежьи озера при условии
# - минимальный угол места - 10 градусов
# - минимальный угол места Солнца для Луны-Глоб - 10 градусов

# Идентификатор наземного пункта - BEAR, система отсчета - BEAR_TOPO.
# Идентификатор посадочного модуля Луна-Глоб - LG_SITE1, система отсчета LG_SITE1_TOPO.

# Построить график: длительность интервала видимости от момента начала интервала.
# На графике изобразить 2 линии: без учета Солнца, с учетом Солнца

#%%

date_beg = '2022 JAN 01'
date_end = '2026 FEB 01'

et_beg = spice.str2et(date_beg)
et_end = spice.str2et(date_end)
et_stp = 86400.0

et = np.arange(et_beg, et_end, et_stp)

#%%

#          target      obs         frame            abcorr  min_angle
params = (('LG_SITE1', 'BEAR',     'BEAR_TOPO',     'CN+S', 10),
          ('SUN',      'LG_SITE1', 'LG_SITE1_TOPO', 'CN+S', 10),
          )

search_wnd = merge_intervals(np.array([[et_beg, et_end]]))

