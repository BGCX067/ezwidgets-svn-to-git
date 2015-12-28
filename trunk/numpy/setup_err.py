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

# err extension module
ezerr = Extension("_ezerr",
                   ["ezerr.i","ezerr.c"],
                   include_dirs = [numpy_include],

                   extra_compile_args = ["--verbose"]
                   )

# NumyTypemapTests setup
setup(  name        = "err test",
        description = "A simple test to demonstrate the use of errno and python exceptions",
        author      = "Egor Zindy",
        version     = "1.0",
        ext_modules = [ezerr]
        )


