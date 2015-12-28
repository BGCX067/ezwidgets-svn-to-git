#! /usr/bin/env python

# System imports
from distutils.core import *
from distutils      import sysconfig

# rev extension module
_rev = Extension("_rev",
                   ["rev.i","rev.c"],
                   include_dirs = [],

                   extra_compile_args = ["--verbose","-march=native","-O9","-ftree-vectorizer-verbose=2","-ffast-math"],
                   swig_opts=['-builtin'],
                   extra_link_args=[],
                   )
if 1:
   _rev.extra_compile_args.append("-fopenmp")
   _rev.extra_link_args.append("-lgomp")


# NumyTypemapTests setup
setup(  name        = "String Reverse Library",
        description = "String Reverse Example",
        author      = "Egor Zindy",
        version     = "1.0",
        ext_modules = [_rev]
        )

