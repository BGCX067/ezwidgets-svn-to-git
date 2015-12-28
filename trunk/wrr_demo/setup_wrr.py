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

# wrr extension module
_wrr = Extension("_wrr",
                   ["wrr.i","wrr.c","myalloc.c"],
                   include_dirs = [numpy_include],

                   #swig_cmd= ["../swig-2.0.5/swig"],
                   extra_compile_args = ["-march=native","-O9","-ffast-math"],
                   #extra_compile_args = ["-ftree-vectorizer-verbose=2","--verbose","-ffast-math"],
                   swig_opts=['-builtin'],
                   extra_link_args=[],
                   )
if 1:
   _wrr.extra_compile_args.append("-fopenmp")
   _wrr.extra_link_args.append("-lgomp")


# NumyTypemapTests setup
setup(  name        = "Weighted Region Ranking",
        description = "Region Ranking adapted from John Gauch's code from 1994",
        author      = "John Gauch / Egor Zindy",
        version     = "1.0",
        ext_modules = [_wrr]
        )
