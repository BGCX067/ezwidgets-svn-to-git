#include <stdio.h>
#include <errno.h>
#include "ezalloc.h"

void alloc(int ni, int** veco, int *n)
{
    int *temp;
    temp = (int *)malloc(ni*sizeof(int));

    if (temp == NULL)
        errno = ENOMEM;

    //veco is either NULL or pointing to the allocated block of memory...
    *veco = temp;
    *n = ni;
}

