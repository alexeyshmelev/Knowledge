import os
import numpy as np
import pandas as pd
import spiceypy as spice


def create_file_list(path):
    """
    Recursive folder listing
    :param path:
    :return:
    """
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]


def load_kernels_from_path(path='kernels', clear=True):
    """
    Load all kernels from klist relative to path.
    :param klist: list of kernel relative paths
    :param path: root kernel path
    :param clear: clear kernel buffer or append kernels
    :return: None
    """
    if clear:
        spice.kclear()

    klist = create_file_list(path)

    for kernel in klist:
        spice.furnsh(kernel)

    return klist


def window2array(cell):
    """
    Convert spice window to numpy array
    """
    return np.array([spice.wnfetd(cell, i) for i in range(spice.wncard(cell))])


def merge_intervals(*arrays, ret_arr=False):
    """
    Merge number of arrays to spice window.
    Arrays should be of (n, 2) shape, where each row is
    interval defined by (left, right) points.
    """
    n = sum(map(len, arrays))
    cell = spice.utils.support_types.SPICEDOUBLE_CELL(2 * n)
    for arr in arrays:
        for (left, right) in arr:
            spice.wninsd(left, right, cell)
    if ret_arr:
        return window2array(cell)
    return cell


def intersect_windows(*windows, ret_arr=False):
    """
    Calculate intersection of number of windows.
    Windows can be spice windows or numpy arrays.
    """
    res_w = windows[0]
    if isinstance(res_w, np.ndarray):
        res_w = merge_intervals(res_w)
    for w in windows[1:]:
        if isinstance(w, np.ndarray):
            w = merge_intervals(w)
        res_w = spice.wnintd(res_w, w)
    if ret_arr:
        return window2array(res_w)
    return res_w


def difference_windows(w0, w1, ret_arr=False):
    """
    Calculate difference between two windows.
    Windows can be spice windows or numpy arrays.
    """
    if isinstance(w0, np.ndarray):
        w0 = merge_intervals(w0)
    if isinstance(w1, np.ndarray):
        w1 = merge_intervals(w1)
    w2 = spice.wndifd(w0, w1)
    if ret_arr:
        return window2array(w2)
    return w2


def window2calendar(wnd, fmt='YYYY-MON-DD HR:MN:SC'):
    """
    Вычисление времени для каоторого существуют данные в датасете
    :param wnd:
    :param fmt:
    :return:
    """
    if isinstance(wnd, np.ndarray):
        return spice.timout(wnd.ravel(), fmt).reshape(-1, 2)
    return spice.timout(window2array(wnd).ravel(), fmt).reshape(-1, 2)


def window2df(wnd, et=False):
    """
    Convert spice window to pandas dataframe in datetime format
    :param wnd: spice window
    :param et: ephemeris time or calendar datetime format?
    :return: df with columns [start, end, duration]
    """
    if et:
        arr = window2array(wnd)
        df = pd.DataFrame({'start': arr[:, 0],
                           'end': arr[:, 1]})
    else:
        arr = window2calendar(wnd, fmt='YYYY-MM-DD HR:MN:SC')
        df = pd.DataFrame({'start': pd.to_datetime(arr[:, 0]),
                           'end': pd.to_datetime(arr[:, 1])})

    df['duration'] = df['end'] - df['start']
    return df


def split_by_max_duration(df, max_duration_hours=24):
    """
    Split dataframe by maximum allowed duration between intervals
    :param df: dataframe with [start, end] columns
    :param max_duration_hours: maximum allowed duration
    :return: list of dataframes
    """
    idx = np.where(df.start - df.end.shift() > np.timedelta64(max_duration_hours, 'h'))[0]
    return np.split(df, idx)