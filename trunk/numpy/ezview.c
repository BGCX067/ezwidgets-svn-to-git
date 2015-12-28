#include <stdio.h>
#include <stdlib.h> 

#include "ezview.h"

void set_ones(double *array, int n)
{
    int i;

    if (array == NULL)
        return;

    for (i=0;i<n;i++)
        array[i] = 1.;
}
