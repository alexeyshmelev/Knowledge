import numpy as np
import types
from scipy.optimize import bisect
from numba import f8, jit, njit


#---------------------------------------------------------------------#
# Thank you to Stan Seibert from the Numba team for help with this
#---------------------------------------------------------------------#
def root_func(x):
    return x**4 - 2*x**2 - x - 3


def compile_specialized_bisect(f):
    """
    Returns a compiled bisection implementation for ``f``.
    """

    def python_bisect(a, b, tol, mxiter):
        """
        Beautiful Docstring ...
        Parameters
        ----------
        a : scalar(int)
            An initial guess
        b : scalar(int)
            An initial guess
        tol : scalar(float)
            The convergence tolerance
        mxiter : scalar(int)
            Max number of iterations to allow
        Note: f(a) should be less than 0 and f(b) should be greater than 0.
              I removed the checks to simplify code.
        """
        its = 0
        fa = jit_root_func(a)
        fb = jit_root_func(b)

        if abs(fa) < tol:
            return a
        elif abs(fb) < tol:
            return b


        c = (a+b)/2.
        fc = jit_root_func(c)

        while abs(fc)>tol and its<mxiter:

            its = its + 1

            if fa*fc < 0:
                b = c
                fb = fc

            else:
                a = c
                fa = fc

            c = (a+b)/2.
            fc = jit_root_func(c)

        return c

    # Have to give explicit type signature for root function to be able
    # to call this function from another nopython function
    jit_root_func = jit('float64(float64)', nopython=True)(root_func)
    return jit(nopython=True)(python_bisect)

jit_bisect_root_func = compile_specialized_bisect(root_func)

print (jit_bisect_root_func(-.5, 50., 1e-8, 500))

#---------------------------------------------------------------------#
#---------------------------------------------------------------------#


def numba_bisect(f, a, b, tol=1e-8, mxiter=500):
    """
    Wraps this stuff up into a single function
    """
    if isinstance(f, types.FunctionType):
        jit_bisect_root_func = compile_specialized_bisect(f)
        return jit_bisect_root_func(a, b, tol, mxiter)
    else:
        return f(a, b, tol, mxiter)


def python_bisect(f, a, b, tol=1e-8, mxiter=500):
    """
    Beautiful Docstring ...
    Parameters
    ----------
    a : scalar(int)
        An initial guess
    b : scalar(int)
        An initial guess
    tol : scalar(float)
        The convergence tolerance
    mxiter : scalar(int)
        Max number of iterations to allow
    Note: f(a) should be less than 0 and f(b) should be greater than 0.
          I removed the checks to simplify code.
    """
    its = 0
    fa = f(a)
    fb = f(b)

    if abs(fa) < tol:
        return a
    elif abs(fb) < tol:
        return b


    c = (a+b)/2.
    fc = f(c)

    while abs(fc)>tol and its<mxiter:

        its = its + 1

        if fa*fc < 0:
            b = c
            fb = fc

        else:
            a = c
            fa = fc

        c = (a+b)/2.
        fc = f(c)

    return c


jit_bisect_root_func = compile_specialized_bisect(root_func)

print(bisect(root_func, -0.5, 50.))
print(python_bisect(root_func, -0.5, 50.))
print(numba_bisect(root_func, -0.5, 50.))

# print("This is the scipy bisect")
# %timeit bisect(root_func, -.5, 50.)
# print("This is the python bisect")
# %timeit python_bisect(root_func, -0.5, 50.)
# print("This is the numba bisect")
# %timeit numba_bisect(jit_bisect_root_func, -0.5, 50.)