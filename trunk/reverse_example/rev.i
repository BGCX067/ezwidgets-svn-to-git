%module rev
%{
#include <errno.h>
#include "rev.h"

%}

%include "cstring.i"
%include "exception.i"

%exception 
{
    errno = 0;
    $action

    if (errno != 0)
    {
        switch(errno)
        {
            case EPERM:
                PyErr_Format(PyExc_IndexError, "Index error");
                break;
            case ENOMEM:
                PyErr_Format(PyExc_MemoryError, "Not enough memory");
                break;
            default:
                PyErr_Format(PyExc_Exception, "Unknown exception");
        }
        SWIG_fail;
    }
}

%apply (char *STRING, size_t LENGTH) { ( unsigned char *s_in, size_t size_in) }

%cstring_output_allocate_size(unsigned char **s_out, size_t *size_out, free(*$1));

%typemap(out) binary_data {
    $result = PyString_FromStringAndSize($1.data,$1.size);
}

%include "rev.h"

