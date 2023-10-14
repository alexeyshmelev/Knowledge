import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

#%%


def hour2float(col) -> float:
    return col.hour + col.minute / 60 + col.second / 3600
#%%

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


plt.figure(figsize=(15, 5))

names = ('LG_SITE1', 'LG_SITE1+SUN')

for name in names:
    df = df_wins[name]
    bottom = hour2float(df.start.dt)
    height = df.duration.dt.total_seconds() / 3600
    plt.bar(df.start.dt.date, height=height, bottom=bottom, width=1.0, alpha=0.7)

# см. пример 3
xax = plt.gca().xaxis
xax.set_major_locator(YearLocator())
xax.set_minor_locator(MonthLocator())
xax.set_major_formatter(DateFormatter('%m\n%Y'))
xax.set_minor_formatter(DateFormatter('%m'))
plt.xlabel('Дата')
plt.ylabel('длительность, ч')
plt.title(f'Карта видимости LG_SITE1 от {date_beg} до {date_end} с наземного пункта BEAR')
plt.grid(which='both', ls='--', alpha=0.5)
plt.tight_layout()
plt.xlim(pd.to_datetime(date_beg), pd.to_datetime(date_end))
plt.show()
