from distutils.core import setup, Extension
import sipdistutils

_factorial = Extension( "factorial",
        ["factorial.sip", "factorial.cpp"],
        include_dirs = ["."],
        extra_compile_args = ["--verbose"],
        extra_link_args=[],
)

setup( name = 'factorial',
        description = "A very simple factorial class written in C++",
        version = '1.0',
        author = "Egor Zindy",
        ext_modules=[ _factorial ],
        cmdclass = {'build_ext': sipdistutils.build_ext}
)

