from distutils.core import setup
from Cython.Build import cythonize

setup(name='Test',
      ext_modules=cythonize("hello_cpp.pyx", language='c++'))

setup(name='Test',
      ext_modules=cythonize("hello.pyx"))

# python setup.py build_ext --inplace

# cythonize -a -i hello.pyx