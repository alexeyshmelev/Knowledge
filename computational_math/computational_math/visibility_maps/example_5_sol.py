import numpy as np
from datetime import timedelta, datetime, time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

#%% Задание

# Для интервалов видимости из предыдущего примера отобразить карту прямоугольниками ширины 1:
# - ось x - дата начала интервала
# - ось y - время начала интервала, время конца интервала
# - корректно обработать интервалы, выходящие за границы суток


#%%
date_beg = '2022 JAN 01'
date_end = '2026 FEB 01'

df_wins = {'LG_SITE1': pd.read_pickle('lg_site1.pkl'),
           'LG_SITE1+SUN': pd.read_pickle('lg_site1_sun.pkl')}

#%%

def hour2float(col) -> float:
    return col.hour + col.minute / 60 + col.second / 3600

def split_interval_to_days(start: datetime, end: datetime) -> pd.DataFrame:
    s = hour2float(start)
    d = (end - start).seconds / 3600

    if s + d > 24:
        res = pd.DataFrame({
            'start': [start, start.date() + timedelta(days=1)],
            'end': [start.date() + timedelta(days=1) - timedelta(microseconds=1), end]})
        res['duration'] = res.end - res.start
    else:
        res = pd.DataFrame({
            'start': [start],
            'end': [end],
            'duration': [end - start]})
    return res

#%%

plt.figure(figsize=(15, 5))

# names = ('LG_SITE1', 'LG_SITE1+SUN')

# lines = {}
# for i, name in enumerate(names):
#     df = df_wins[name]
#     dfs = [split_interval_to_days(row.start, row.end) for _, row in df.iterrows()]
#     df_full = pd.concat(dfs)
#
#     bottom = hour2float(df_full.start.dt)
#     height = df_full.duration.dt.total_seconds() / 3600
#     line = plt.bar(df_full.start.dt.date, height=height, bottom=bottom, width=1.0, alpha=0.7)
#     lines[i] = line

df = df_wins['LG_SITE1+SUN']
dfs = [split_interval_to_days(row.start, row.end) for _, row in df.iterrows()]
df_full = pd.concat(dfs)

bottom = hour2float(df_full.start.dt)
height = df_full.duration.dt.total_seconds() / 3600
line = plt.bar(df_full.start.dt.date, height=height, bottom=bottom, width=1.0, alpha=0.7)

# см. пример 3
xax = plt.gca().xaxis
xax.set_major_locator(YearLocator())
xax.set_minor_locator(MonthLocator())
xax.set_major_formatter(DateFormatter('%m\n%Y'))
xax.set_minor_formatter(DateFormatter('%m'))
plt.xlabel('Дата')
plt.ylabel('длительность, ч')
plt.title(f'Карта видимости LG_SITE1 от {date_beg} до {date_end} с наземного пункта BEAR')
plt.grid(axis='y', which='major', ls='--', alpha=0.5)
plt.grid(axis='x', which='minor', ls='--', alpha=0.5)
plt.grid(axis='x', which='major', ls='--')
plt.tight_layout()
plt.xlim(pd.to_datetime(date_beg), pd.to_datetime(date_end))
plt.ylim(0, 24)
plt.yticks(np.arange(25))
plt.legend(line, ['LG_SITE1+SUN'])
plt.show()

