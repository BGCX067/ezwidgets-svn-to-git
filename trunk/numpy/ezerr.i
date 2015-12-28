%module ezerr
%{
#include <errno.h>
#include "ezerr.h"

#define SWIG_FILE_WITH_INIT
%}

%include "numpy.i"

%init %{
    import_array();
%}

%exception
{
    errno = 0;
    $action

    if (errno != 0)
    {
        switch(errno)
        {
            case EPERM:
                PyErr_Format(PyExc_IndexError, "Index out of range");
                break;
            case ENOMEM:
                PyErr_Format(PyExc_MemoryError, "Failed malloc()");
                break;
            default:
                PyErr_Format(PyExc_Exception, "Unknown exception");
        }
        SWIG_fail;
    }
}

%apply (int* IN_ARRAY1, int DIM1) {(int *array, int n)}

%include "ezerr.h"

