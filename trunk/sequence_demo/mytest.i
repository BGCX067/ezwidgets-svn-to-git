%module mytest
%{
#include <errno.h>
#include "mytest.h"

#define SWIG_FILE_WITH_INIT
%}

%include "numpy.i"
%include "exception.i"

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
            case ENOMEM:
                PyErr_Format(PyExc_MemoryError, "Not enough memory");
                break;
            case E2BIG:
                PyErr_Format(PyExc_ValueError, "Background image array size mismatch");
                break;
            case EPERM:
                PyErr_Format(PyExc_ValueError, "Not a 3 channel OpenCV image array");
                break;
            default:
                PyErr_Format(PyExc_Exception, "Unknown exception");
        }
        SWIG_fail;
    }
}

%apply (unsigned char* IN_ARRAY3, int DIM1, int DIM2, int DIM3) {(unsigned char *ArrayIn, int Ydim, int Xdim, int Cdim)}
%apply (unsigned char** IN_ARRAY3, int DIM1, int DIM2, int DIM3) {(unsigned char **ArrayIn, int Zdim, int Ydim, int Xdim)}
%apply (unsigned char* IN_ARRAY2, int DIM1, int DIM2) {(unsigned char *ArrayIn2, int Ydim2, int Xdim2)}
%apply (unsigned char** ARGOUTVIEWM_ARRAY2, int* DIM1, int* DIM2) {(unsigned char **pArrayOut, int *YdimOut, int *XdimOut)}
%apply (unsigned char** INPLACE_ARRAY3, int DIM1, int DIM2, int DIM3) {(unsigned char **ArrayInpl, int Zdim, int Ydim, int Xdim)}

%include "mytest.h"

