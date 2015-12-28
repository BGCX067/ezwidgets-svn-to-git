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

# view extension module
_ezview = Extension("_ezview",
                   ["ezview.i","ezview.c"],
                   include_dirs = [numpy_include],
                   )

# NumyTypemapTests setup
setup(  name        = "ezview module",
        description = "ezview provides 3 functions: set_ones(), get_view() and finalize(). "
        "set_ones() and get_view() provide a view on a memory block allocated in C, "
        "finalize() takes care of the memory deallocation.",
        author      = "Egor Zindy",
        version     = "1.0",
        ext_modules = [_ezview]
        )


