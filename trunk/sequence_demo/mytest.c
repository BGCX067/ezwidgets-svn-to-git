#include <stdlib.h>
#include <errno.h>
#include <omp.h>
 
#include "mytest.h"

/**
 * make the opencv image (ordered BGR) grayscale using R*0.30 G*0.59 B*0.11
 *
 * @param  ArrayIn    An colour opencv image array (ordered BGB)
 * @param  Ydim       The height of the images
 * @param  Xdim       The width of the images
 * @param  Cdim       The number of colour channel (must be 3)
 * @param  pArrayOut  A pointer to the output grayscale image array
 * @param  YdimOut    The height of the image
 * @param  XdimOut    The width of the image
 */
void grayscale(unsigned char *ArrayIn, int Ydim, int Xdim, int Cdim, unsigned char **pArrayOut, int *YdimOut, int *XdimOut)
{
    int i,j;
    float temp;
    unsigned char *ArrayOut = NULL;

    if (Cdim!=3)
    {
        errno = EPERM;
        goto end;
    }

    //allocating memory for the output image
    if (*pArrayOut == NULL) {
        *pArrayOut = (unsigned char *)malloc(Ydim*Xdim*sizeof(unsigned char));
    }
    ArrayOut = *pArrayOut;

    if (ArrayOut == NULL) {
        errno = ENOMEM;
        goto end;
    }

    #pragma omp parallel for        \
        default(shared) private(j,temp)

    for (i = 0; i< Ydim*Xdim; i++)
    {
        j = i*3;
        temp = 0.11*ArrayIn[j] + 0.59*ArrayIn[j+1] + 0.3*ArrayIn[j+2];
        ArrayOut[i] = (unsigned char)temp;
    }

end:
    *pArrayOut = ArrayOut;
    *YdimOut = Ydim;
    *XdimOut = Xdim;
}

/**
 * Perform numpy.average(stack,axis=0)
 *
 * @param  ArrayIn    An array of pointers to the slices (contiguous Ydim*Xdim memory block, one for each slice)
 * @param  Zdim       The number of slices
 * @param  Ydim       The height of the images
 * @param  Xdim       The width of the images
 * @param  pArrayOut  A pointer to the output averaged image
 * @param  YdimOut    The height of the image
 * @param  XdimOut    The width of the image
 */
void average(unsigned char **ArrayIn, int Zdim, int Ydim, int Xdim, unsigned char **pArrayOut, int *YdimOut, int *XdimOut)
{
    int z,i;

    unsigned char *ArrayOut = NULL;
    float temp;

    //allocating memory for the output image
    if (*pArrayOut == NULL) {
        *pArrayOut = (unsigned char *)calloc(Ydim*Xdim,sizeof(unsigned char));
    }
    ArrayOut = *pArrayOut;

    if (ArrayOut == NULL) {
        errno = ENOMEM;
        goto end;
    }

    #pragma omp parallel for        \
        default(shared) private(z,temp)

    for (i = 0; i < Ydim*Xdim; i++)
    {
        temp = 0;
        for (z = 0; z < Zdim; z++)
        {
            temp += ArrayIn[z][i];
        }
        temp = temp / Zdim;
        if (temp > 255)
            temp = 255;

        ArrayOut[i] = (unsigned char)temp;
    }

end:
    *pArrayOut = ArrayOut;
    *YdimOut = Ydim;
    *XdimOut = Xdim;
}

/**
 * For each slice in the list, replace the pixel values with abs(pixel value - background pixel value)
 *
 * @param  ArrayInpl  an array of pointers to the slices (contiguous Ydim*Xdim memory block)
 * @param  Zdim       The number of slices
 * @param  Ydim       The height of the images
 * @param  Xdim       The width of the images
 * @param  ArrayIn2   The background image array (must be the same size as Ydim,Xdim)
 * @param  Ydim2      The height of the background image
 * @param  Xdim2      The width of the background image
 */
void bsub(unsigned char **ArrayInpl, int Zdim, int Ydim, int Xdim, unsigned char *ArrayIn2, int Ydim2, int Xdim2)
{
    int i,z;

    if (Ydim!=Ydim2 || Xdim!=Xdim2) {
        errno = E2BIG;
        goto end;
    }

    #pragma omp parallel for        \
        default(shared) private(i)

    for (z = 0; z < Zdim; z++)
    {
        for (i = 0; i< Ydim*Xdim; i++)
            ArrayInpl[z][i] = abs(ArrayInpl[z][i]-ArrayIn2[i]);
    }

end:
    return;
}
