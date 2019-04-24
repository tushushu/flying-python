"""
@Author: tushushu
@Date: 2019-04-24 16:11:52
"""

# Makes pyximport compatible with cpp! 
# import pyx2cpp; pyx2cpp.install()
# https://stackoverflow.com/questions/21938065/how-to-configure-pyximport-to-always-make-a-cpp-file

import pyximport
from pyximport import install

old_get_distutils_extension = pyximport.pyximport.get_distutils_extension

def new_get_distutils_extension(modname, pyxfilename, language_level=3):
    extension_mod, setup_args = old_get_distutils_extension(modname, pyxfilename, language_level)
    extension_mod.language='c++'
    return extension_mod,setup_args

pyximport.pyximport.get_distutils_extension = new_get_distutils_extension