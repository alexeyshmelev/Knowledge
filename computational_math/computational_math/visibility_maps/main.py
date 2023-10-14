import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import spiceypy as spice
from utils import (load_kernels_from_path, merge_intervals, window2df, split_by_max_duration, intersect_windows, window2calendar)
from datetime import timedelta, datetime, time
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import subprocess

load_kernels_from_path(path='kernels')


def hour2float(col) -> float:
    """
    Перевод часов в десятичный вид
    :param col: время
    :return:
    """
    return col.hour + col.minute / 60 + col.second / 3600


def split_interval_to_days(start: datetime, end: datetime) -> pd.DataFrame:
    """
    Разбиение по дням
    :param start: начало интервала видимости
    :param end: конец интервала видимости
    :return:
    """
    s = hour2float(start)
    d = (end - start).seconds / 3600

    if s + d > 24:
        res = pd.DataFrame({
            'start': [start, start.date() + timedelta(days=1)],
            'end': [start.date() + timedelta(days=1) - timedelta(microseconds=1), end]})
        res['duration'] = res.end - res.start
    elif (end - start).days > 1:
        dfs = []
        start_s = start
        while start_s.date() <= end.date():
            if end.date() - start_s.date() >= timedelta(days=1):
                res = pd.DataFrame({
                    'start': [start_s],
                    'end': [start_s + timedelta(days=1) - timedelta(microseconds=1)]})
            else:
                res = pd.DataFrame({
                    'start': [start_s],
                    'end': [end]})
            start_s += timedelta(days=1)
            res['duration'] = res.end - res.start
            dfs.append(res)
        res = pd.concat(dfs)
    else:
        res = pd.DataFrame({
            'start': [start],
            'end': [end],
            'duration': [end - start]})
    return res

loc = ['BEAR', 'USSURIYSK']
cases = [['SUN', 'LG_SITE1', 5],
         ['-551'],
         ['-172'],
         ['MARS']]

legends = ['Луна-Глоб', 'Спектр-РГ', 'Экзомарс', 'Марс']

for l in loc:
    plt.figure(figsize=(15, 5))
    lines = []
    for cn, c in enumerate(cases):

        if cn == 2:
            dt = window2calendar(spice.spkcov('kernels/spk/exomars.bsp', -172))
            date_beg = datetime.strftime(datetime.strptime(' '.join(dt[0][0].split(' ')[0].split('-')), '%Y %b %d') + timedelta(days=1), '%Y %b %d')
            date_end = datetime.strftime(datetime.strptime(' '.join(dt[0][1].split(' ')[0].split('-')), '%Y %b %d') - timedelta(days=1), '%Y %b %d')
            print(dt, date_beg, date_end)

        elif cn == 3:
            output = subprocess.run(["brief.exe", "-c", "kernels/spk/mar097_2022_2032.bsp"], capture_output=True, text=True).stdout.split(' ')
            for i, word in enumerate(output):
                if word == 'MARS' and output[i+1][0] == '(':
                    num = int(output[i+1][1:-1])
            dt = window2calendar(spice.spkcov('kernels/spk/mar097_2022_2032.bsp', num))
            date_beg = datetime.strftime(datetime.strptime(' '.join(dt[0][0].split(' ')[0].split('-')), '%Y %b %d') + timedelta(days=1), '%Y %b %d')
            date_end = '2026 FEB 01'

        else:
            date_beg = '2022 JAN 01'
            date_end = '2026 FEB 01'

        et_beg = spice.str2et(date_beg)
        et_end = spice.str2et(date_end)
        et_stp = 86400.0
        et = np.arange(et_beg, et_end, et_stp)

        if cn == 0:
            params = (('LG_SITE1', l, f'{l}_TOPO', 'CN+S', 10),
                      (c[0], c[1], f'{c[1]}_TOPO', 'CN+S', c[2]) if cn==0 else (c[0], l, f'{l}_TOPO', 'CN+S', 10))
        else:
            params = ((c[0], c[1], f'{c[1]}_TOPO', 'CN+S', c[2]) if cn == 0 else (c[0], l, f'{l}_TOPO', 'CN+S', 10),)

        search_wnd = merge_intervals(np.array([[et_beg, et_end]]))

        windows = {}

        for trg, obs, frm, abc, min_angle in params:
            cell = spice.utils.support_types.SPICEDOUBLE_CELL(10000)
            window = spice.gfposc(trg, frm, abc, obs,
                                  'LATITUDINAL', 'LATITUDE', '>', np.deg2rad(min_angle),
                                  0.0, 600, 10000, search_wnd, cell)
            windows[trg] = window

        windows['OBJ+SUN'] = intersect_windows(*windows.values())

        df_wins = {key: window2df(win) for key, win in windows.items()}
        df_wins['OBJ+SUN'].to_pickle(f'{l}_{c[0]}.pkl')
        df_wins['OBJ+SUN'].to_csv(f'{l}_{c[0]}.csv')

        df = pd.read_pickle(f'{l}_{c[0]}.pkl')
        dfs = [split_interval_to_days(row.start, row.end) for _, row in df.iterrows()]
        df_full = pd.concat(dfs)

        bottom = hour2float(df_full.start.dt)
        height = df_full.duration.dt.total_seconds() / 3600
        lines.append(plt.bar(df_full.start.dt.date, height=height, bottom=bottom, width=1.0, alpha=0.7))

    xax = plt.gca().xaxis
    xax.set_major_locator(YearLocator())
    xax.set_minor_locator(MonthLocator())
    xax.set_major_formatter(DateFormatter('%m\n%Y'))
    xax.set_minor_formatter(DateFormatter('%m'))
    plt.xlabel('Дата')
    plt.ylabel('длительность, ч')
    plt.title(f'Карта видимости объектов от {date_beg} до {date_end} с наземного пункта {l}')
    plt.grid(axis='y', which='major', ls='--', alpha=0.5)
    plt.grid(axis='x', which='minor', ls='--', alpha=0.5)
    plt.grid(axis='x', which='major', ls='--')
    plt.tight_layout()
    plt.xlim(pd.to_datetime('2022 JAN 01'), pd.to_datetime('2026 FEB 01'))
    plt.ylim(0, 24)
    plt.yticks(np.arange(25))
    plt.legend(lines, legends)
    plt.savefig(f'{l}.png')

