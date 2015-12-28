#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include "rev.h"
#include "omp.h"

void reverse(unsigned char *s_in, size_t size_in, unsigned char **s_out, size_t *size_out)
{
    size_t i;
    unsigned char *ptr = NULL;

    //output array can be passed to the function, but need to check its size. OK if larger, but not smaller.
    if (*s_out == NULL)
        ptr = (unsigned char *)malloc(size_in*sizeof(unsigned char));
    else
    {
        if (*size_out < size_in)
        {
            errno = EPERM;
            goto end;
        }
        ptr = *s_out;
    }

    //check the arrays
    if (ptr == NULL)
    {
        errno = ENOMEM;
        goto end;
    }

    *s_out = ptr;
    ptr += (size_in - 1);

    #pragma omp parallel for        \
        default(shared) private(i)

    for (i=0 ; i<size_in; i++)
    {
        *(ptr-i) = *(s_in+i);
    }

end:
    *size_out = size_in;
}

binary_data revstruct(unsigned char *s_in, size_t size_in)
{
    binary_data result;
    result.data = NULL;
    reverse(s_in,size_in,&(result.data),&(result.size));
    return result;
}

