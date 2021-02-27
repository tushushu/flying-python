"""
@Author: tushushu
@Date: 2019-06-20 10:32:30
"""

from distutils.core import setup
from Cython.Build import cythonize
import numpy


def compile_file(file_name: str):
    """Compile pyx file."""

    ext_modules = cythonize(file_name)
    name = file_name.split(".")[0] if "." in file_name else file_name
    setup(name=name, ext_modules=ext_modules, include_dirs=[numpy.get_include()])


if __name__ == "__main__":
    compile_file("utils.pyx")

# source activate py36
# python setup.py build_ext --inplace
