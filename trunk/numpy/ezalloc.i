%module ezalloc
%{
#include <errno.h>
#include "ezalloc.h"

#define SWIG_FILE_WITH_INIT
%}

%include "numpy.i"

%init %{
    import_array();
%}

%apply (int** ARGOUTVIEWM_ARRAY1, int *DIM1) {(int** veco1, int* n1)}
%apply (int** ARGOUTVIEW_ARRAY1, int *DIM1) {(int** veco2, int* n2)}

%include "ezalloc.h"

%exception
{
    errno = 0;
    $action

    if (errno != 0)
    {
        switch(errno)
        {
            case ENOMEM:
                PyErr_Format(PyExc_MemoryError, "Failed malloc()");
                break;
            default:
                PyErr_Format(PyExc_Exception, "Unknown exception");
        }
        SWIG_fail;
    }
}

%rename (alloc_managed) my_alloc1;
%rename (alloc_leaking) my_alloc2;

%inline %{

void my_alloc1(int ni, int** veco1, int *n1)
{
    /* The function... */
    alloc(ni, veco1, n1);
}

void my_alloc2(int ni, int** veco2, int *n2)
{
    /* The function... */
    alloc(ni, veco2, n2);
}

%}


