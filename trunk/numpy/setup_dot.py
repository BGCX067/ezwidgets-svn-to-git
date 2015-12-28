#! /usr/bin/env python

# System imports
from distutils.core import *
from distutils      import sysconfig

# Third-party modules - we depend on numpy for everything
import numpy

# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

# dot extension module
_dot = Extension("_dot",
                   ["dot.i","dot.c"],
                   include_dirs = [numpy_include],
                   )

# NumyTypemapTests setup
setup(  name        = "Dot product",
        description = "Function that performs a dot product (numpy.i: a SWIG Interface File for NumPy)",
        author      = "Egor Zindy (based on the setup.py file available in the numpy tree)",
        version     = "1.0",
        ext_modules = [_dot]
        )

