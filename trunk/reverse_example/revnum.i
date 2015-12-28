%module revnum
%{
#include <errno.h>
#include "rev.h"

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

%apply (unsigned char* IN_ARRAY1, int DIM1) {(unsigned char *s_in, size_t size_in)}
%apply (unsigned char** ARGOUTVIEWM_ARRAY1, int* DIM1) {(unsigned char **s_out, size_t *size_out)}

void reverse(unsigned char *s_in, size_t size_in, unsigned char **s_out, size_t *size_out);

%apply (unsigned char* INPLACE_ARRAY1, size_t DIM1) {(unsigned char *s_in, size_t size_in)}

%inline %{

void inplace(unsigned char *s_in, size_t size_in)
{
    size_t i;
    unsigned char temp, *ptr = NULL;

    ptr = s_in + (size_in - 1);

    #pragma omp parallel for        \
        default(shared) private(i,temp)

    for (i=0 ; i<size_in/2; i++)
    {
        temp = *(ptr-i);
        *(ptr-i) = *(s_in+i);
        *(s_in+i) = temp;
    }
}

%}

