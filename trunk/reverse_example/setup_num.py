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

# revnum extension module
_revnum = Extension("_revnum",
                   ["revnum.i","rev.c"],
                   include_dirs = [numpy_include],

                   extra_compile_args = ["--verbose","-march=native","-O9","-ftree-vectorizer-verbose=2","-ffast-math"],
                   swig_opts=['-builtin'],
                   extra_link_args=[],
                   )
if 1:
   _revnum.extra_compile_args.append("-fopenmp")
   _revnum.extra_link_args.append("-lgomp")


# NumyTypemapTests setup
setup(  name        = "String Reverse Library",
        description = "String Reverse Example (numpy integration)",
        author      = "Egor Zindy",
        version     = "1.0",
        ext_modules = [_revnum]
        )

