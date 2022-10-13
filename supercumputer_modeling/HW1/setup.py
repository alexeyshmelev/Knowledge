from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy


ext = Extension("code_cython", ["code_cython.pyx"],
                include_dirs = [numpy.get_include(),
                                '.'],
                language='c',
                extra_compile_args=['-Ofast', '-march=native'],
                annotate=True)

setup(ext_modules=[ext],
      cmdclass = {'build_ext': build_ext})
