from distutils.core import setup, Extension
import sipdistutils

_example = Extension( "example",
        ["example.sip", "example.c"],
        include_dirs = [],
        extra_compile_args = ["--verbose"],
        extra_link_args=[],
)

setup( name = 'example',
        description = "A very simple example copied from SWIG's",
        version = '1.0',
        author = "Egor Zindy",
        ext_modules=[ _example ],
        cmdclass = {'build_ext': sipdistutils.build_ext}
)
