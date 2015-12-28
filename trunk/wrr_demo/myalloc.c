#include <stdlib.h>
#include <errno.h>
 
#include "myalloc.h"

void **make_strides(void *Image, int Ydim, int Xdim, size_t size) 
{
    char *ptr;
    void **out = NULL;
    size_t stride;
    int i;

    if (Image == NULL)
    {
        errno = ENOMEM;
        goto end;
    }

    //assumes pointers are all the same size.
    out = (void **)malloc(Ydim*sizeof(void *));
    if (out == NULL)
    {
        errno = ENOMEM;
        goto end;
    }

    //stride is image line size bytes
    stride = size * Xdim;
    
    //we're using a char pointer for 1 byte increments.
    ptr = (char *)Image;

    for (i=0; i<Ydim; i++)
    {
        out[i] = (void *)ptr;
        //now can increment ptr in bytes using stride
        ptr+=stride;
    }

end:
    return out;
}



