#include <stdlib.h>
#include <errno.h>

#include "ezerr.h"

//return the array element defined by index
int val(int *array, int n, int index)
{
    int value=0;

    if (index < 0 || index >=n)
    {
        errno = EPERM;
        goto end;
    }

    value = array[index];

end:
    return value;
}

//allocate (and free) a char array of size n
void alloc(int n)
{
    char *array;

    array = (char *)malloc(n*sizeof(char));
    if (array == NULL)
    {
        errno = ENOMEM;
        goto end;
    }

    //don't keep the memory allocated...
    free(array);

end:
    return;
}

