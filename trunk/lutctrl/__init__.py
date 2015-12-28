__all__ = []

package_list = ['ctrl','data']

for subpackage in package_list:
    try: 
        exec 'import ' + subpackage
        __all__.append( subpackage )
    except ImportError:
        pass

#testing...
from test import test
