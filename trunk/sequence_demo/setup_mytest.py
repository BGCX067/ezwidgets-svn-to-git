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

# mytest extension module
_mytest = Extension("_mytest",
                   ["mytest.i","mytest.c"],
                   include_dirs = [numpy_include],

                   #swig_cmd= ["../swig-2.0.5/swig"],
                   extra_compile_args = ["--verbose","-march=native","-O9","-ftree-vectorizer-verbose=2","-ffast-math"],
                   swig_opts=['-builtin'],
                   extra_link_args=[],
                   )
if 1:
   _mytest.extra_compile_args.append("-fopenmp")
   _mytest.extra_link_args.append("-lgomp")


# NumyTypemapTests setup
setup(  name        = "mytest",
        description = "Testing the new typemaps",
        author      = "Egor Zindy",
        version     = "1.0",
        ext_modules = [_mytest]
        )

