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

print(f"{et_beg=}", f"{et_end=}", sep='\n')


#%% Определяем параметры расчета

#          target      obs         frame            abcorr  min_angle
params = (('LG_SITE1', 'BEAR',     'BEAR_TOPO',     'CN+S', 10),
          ('-551',      'BEAR', 'BEAR_TOPO', 'CN+S', 10),
          )

search_wnd = merge_intervals(np.array([[et_beg, et_end]]))

windows = {}
for trg, obs, frm, abc, min_angle in params:
    cell = spice.utils.support_types.SPICEDOUBLE_CELL(10000)
    window = spice.gfposc(trg, frm, abc, obs,
                          'LATITUDINAL', 'LATITUDE', '>', np.deg2rad(min_angle),
                          0.0, 600, 10000, search_wnd, cell)
    windows[trg] = window

#%%
windows['LG_SITE1+SUN'] = intersect_windows(*windows.values())

df_wins = {key: window2df(win) for key, win in windows.items()}

#%% Сохраняем датафреймы для следующего примера

df_wins['LG_SITE1'].to_pickle('lg_site1.pkl')
df_wins['LG_SITE1+SUN'].to_pickle('lg_site1_sun.pkl')

#%% Строим простой график длительности интервалов видимости

plt.figure(figsize=(15, 5))
for name in ('LG_SITE1', 'LG_SITE1+SUN'):
    df = df_wins[name]
    plt.plot(df.start, df.duration.dt.seconds / 3600, label=name)
plt.legend()
plt.show()

#%%
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib

colors = matplotlib.rcParams['axes.prop_cycle'].by_key()['color']

#%%
plt.figure(figsize=(15, 5))

names = ('LG_SITE1', 'LG_SITE1+SUN')

lines = {}
for i, name in enumerate(names):
    df = df_wins[name]
    dfs = split_by_max_duration(df, max_duration_hours=24)

    for df_ in dfs:
        line = plt.plot(df_.start, df_.duration.dt.seconds / 3600, color=colors[i])
        lines[i] = line[0]

ax = plt.gca()
ax.xaxis.set_major_locator(YearLocator())
ax.xaxis.set_minor_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter('%m\n%Y'))
ax.xaxis.set_minor_formatter(DateFormatter('%m'))
plt.xlabel('Дата')
plt.ylabel('длительность, ч')
plt.title(f'Длительность видимости LG_SITE1 от {date_beg} до {date_end} '
          f'с наземного пункта BEAR')
plt.yticks(np.arange(25))
plt.grid(axis='y', which='major', ls='--', alpha=0.5)
plt.grid(axis='x', which='minor', ls='--', alpha=0.5)
plt.grid(axis='x', which='major', ls='--')
plt.tight_layout()
plt.xlim(pd.to_datetime(date_beg), pd.to_datetime(date_end))
plt.legend(lines.values(), names)
plt.show()

