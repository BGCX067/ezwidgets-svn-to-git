/*---------------------------------------------------------------------------*/
/* Program:  wrr.c                                                           */
/*                                                                           */
/* Purpose:  This program performs local contrast enhancement by computing   */
/*           the weighted region ranking (WRR) for each pixel in the image.  */
/*           Two parameters control this process:                            */
/*                                                                           */
/*           1)  The size of the contextual region about each pixel is       */
/*           specified by the standard deviation of a Gaussian weighting     */
/*           function.  The values of this function control the amount       */
/*           each pixel in the contextual region contributes to the pseudo-  */
/*           histogram and hence the rank of each pixel.  Like WAHE this     */
/*           provides a smooth transition from pixels in the contextual      */
/*           region to those outside.                                        */
/*                                                                           */
/*           2)  The amount of contrast enhancement of each pixel is         */
/*           specified by the standard deviation of a Gaussian smoothing     */
/*           function.  By blurring the pseudo-histogram the first and       */
/*           second derivatives of the cumulative histogram are reduced.     */
/*           Like CLAHE this reduces the contrast enhancement at each        */
/*           pixel.  Unlike CLAHE this method reduces the rate of change     */
/*           of contrast enhancement.                                        */
/*                                                                           */
/* Author:   John Gauch                                                      */
/*                                                                           */
/* Date:     April 22, 1994                                                  */
/*                                                                           */
/* Note:     Copyright (C) The University of Kansas, 1994                    */
/*           Modified by Egor Zindy to use with OpenMP and Python, 2012      */
/*---------------------------------------------------------------------------*/

#include <stdlib.h>
#include <errno.h>
#include <math.h>
#include <omp.h>
 
#include "wrr.h"
#include "myalloc.h"

void wrr(int *ImageIn, int Ydim, int Xdim, int nbits, float BlurStdDev, float WeightStdDev, int Radius, int Step, int **ImageOut, int *YdimOut, int *XdimOut)
{
    int x, y, dx, dy;
    float Variance;
    float *ImageWeight = NULL;
    float **Weight = NULL;

    float Temp, Area, Below, Blur;
    int Center;
    int weight_size;
    int **Data1 = NULL, **Data2 = NULL;
    int max_level = (int)(pow(2,nbits)) - 1;

    /* Allocate weight array */
    weight_size = (2 * Radius + 1);
    ImageWeight = (float *)malloc(weight_size * weight_size * sizeof(float));
    Weight = (float **)make_strides(ImageWeight, weight_size, weight_size, sizeof(float));

    /* Allocate input stride array */
    Data1 = (int **)(make_strides(ImageIn, Ydim, Xdim, sizeof(int)));

    /* Allocate output array */
    *ImageOut = (int *)malloc(Ydim*Xdim*sizeof(int));
    Data2 = (int **)(make_strides(*ImageOut, Ydim, Xdim, sizeof(int)));

    /* Was all the memory allocation successful? */
    if (ImageWeight == NULL || Weight == NULL || Data1 == NULL || *ImageOut == NULL || Data2 == NULL)
    {
        errno = ENOMEM;
        goto end;
    }

    /* Initialize weight table */
    Variance = 2 * WeightStdDev * WeightStdDev;

    for (dy = -Radius; dy <= Radius; dy++)
    {
        for (dx = -Radius; dx <= Radius; dx++)
        {
            Weight[dy + Radius][dx + Radius] = (float) exp(-(dx * dx + dy * dy) / Variance);
        }
    }

    /* Handle case without histogram blurring */
    if (BlurStdDev <= 1)
    {
        for (y = 0; y < Ydim; y++)
            for (x = 0; x < Xdim; x++)
            {
                /* Consider neighborhood radius R about point */
                Area = 0.0;
                Below = 0.0;
                Center = Data1[y][x];

                for (dy = -Radius; dy <= Radius; dy+=Step)
                    for (dx = -Radius; dx <= Radius; dx+=Step)
                    {
                        if ((y + dy >= 0) && (y + dy < Ydim - 1) && (x + dx >= 0) && (x + dx < Xdim - 1))
                        {
                            Temp = Weight[dy + Radius][dx + Radius];
                            Area += Temp;
                            if (Data1[y + dy][x + dx] < Center)
                                Below += Temp;
                        }
                    }
                Data2[y][x] = max_level * Below / Area;
            }
    }

    /* Handle slower case with histogram blurring */
    else
    {
        for (y = 0; y < Ydim; y++)
            for (x = 0; x < Xdim; x++)
            {
                /* Consider neighborhood radius R about point */
                Area = 0.0;
                Below = 0.0;
                Center = Data1[y][x];

                for (dy = -Radius; dy <= Radius; dy+=Step)
                    for (dx = -Radius; dx <= Radius; dx+=Step)
                    {
                        if ((y + dy >= 0) && (y + dy < Ydim - 1) && (x + dx >= 0) && (x + dx < Xdim - 1))
                        {
                            Blur = (Center - Data1[y + dy][x + dx]) / BlurStdDev;
                            if (Blur < 0) Blur = 0;
                            else if (Blur > 1) Blur = 1;

                            Temp = Weight[dy + Radius][dx + Radius];
                            Area += Temp;
                            Below += Temp * Blur;
                        }
                    }
                Data2[y][x] = max_level * Below / Area;
            }
    }

end:
    if (ImageWeight != NULL) free(ImageWeight);
    if (Weight != NULL) free(Weight);
    if (Data1 != NULL) free(Data1);
    if (Data2 != NULL) free(Data2);

    *YdimOut = Ydim;
    *XdimOut = Xdim;
}

void parallel_wrr(int *ImageIn, int Ydim, int Xdim, int nbits, float BlurStdDev, float WeightStdDev, int Radius, int Step, int **ImageOut, int *YdimOut, int *XdimOut)
{
    int x, y, dx, dy;
    float Variance;
    float *ImageWeight = NULL;
    float **Weight = NULL;

    float Temp, Area, Below, Blur;
    int Center;
    int weight_size;
    int **Data1 = NULL, **Data2 = NULL;
    int max_level = (int)(pow(2,nbits)) - 1;

    /* Allocate weight array */
    weight_size = (2 * Radius + 1);
    ImageWeight = (float *)malloc(weight_size * weight_size * sizeof(float));
    Weight = (float **)make_strides(ImageWeight, weight_size, weight_size, sizeof(float));

    /* Allocate input stride array */
    Data1 = (int **)(make_strides(ImageIn, Ydim, Xdim, sizeof(int)));

    /* Allocate output array */
    *ImageOut = (int *)malloc(Ydim*Xdim*sizeof(int));
    Data2 = (int **)(make_strides(*ImageOut, Ydim, Xdim, sizeof(int)));

    /* Was all the memory allocation successful? */
    if (ImageWeight == NULL || Weight == NULL || Data1 == NULL || *ImageOut == NULL || Data2 == NULL)
    {
        errno = ENOMEM;
        goto end;
    }

    /* Initialize weight table */
    Variance = 2 * WeightStdDev * WeightStdDev;

    for (dy = -Radius; dy <= Radius; dy++)
    {
        for (dx = -Radius; dx <= Radius; dx++)
        {
            Weight[dy + Radius][dx + Radius] = (float) exp(-(dx * dx + dy * dy) / Variance);
        }
    }

    /* Handle case without histogram blurring */
    if (BlurStdDev <= 1)
    {
        #pragma omp parallel for        \
            default(shared) private(x,dy,dx,Area,Below,Center,Temp)

        for (y = 0; y < Ydim; y++)
            for (x = 0; x < Xdim; x++)
            {
                /* Consider neighborhood radius R about point */
                Area = 0.0;
                Below = 0.0;
                Center = Data1[y][x];

                for (dy = -Radius; dy <= Radius; dy+=Step)
                    for (dx = -Radius; dx <= Radius; dx+=Step)
                    {
                        if ((y + dy >= 0) && (y + dy < Ydim - 1) && (x + dx >= 0) && (x + dx < Xdim - 1))
                        {
                            Temp = Weight[dy + Radius][dx + Radius];
                            Area += Temp;
                            if (Data1[y + dy][x + dx] < Center)
                                Below += Temp;
                        }
                    }
                Data2[y][x] = max_level * Below / Area;
            }
    }

    /* Handle slower case with histogram blurring */
    else
    {
        #pragma omp parallel for        \
            default(shared) private(x,dy,dx,Area,Below,Center,Temp, Blur)

        for (y = 0; y < Ydim; y++)
            for (x = 0; x < Xdim; x++)
            {
                /* Consider neighborhood radius R about point */
                Area = 0.0;
                Below = 0.0;
                Center = Data1[y][x];

                for (dy = -Radius; dy <= Radius; dy+=Step)
                    for (dx = -Radius; dx <= Radius; dx+=Step)
                    {
                        if ((y + dy >= 0) && (y + dy < Ydim - 1) && (x + dx >= 0) && (x + dx < Xdim - 1))
                        {
                            Blur = (Center - Data1[y + dy][x + dx]) / BlurStdDev;
                            if (Blur < 0) Blur = 0;
                            else if (Blur > 1) Blur = 1;

                            Temp = Weight[dy + Radius][dx + Radius];
                            Area += Temp;
                            Below += Temp * Blur;
                        }
                    }
                Data2[y][x] = max_level * Below / Area;
            }
    }

end:
    if (ImageWeight != NULL) free(ImageWeight);
    if (Weight != NULL) free(Weight);
    if (Data1 != NULL) free(Data1);
    if (Data2 != NULL) free(Data2);

    *YdimOut = Ydim;
    *XdimOut = Xdim;
}

void rr(int *ImageIn, int Ydim, int Xdim, int nbits, int Radius, int Step, int **ImageOut, int *YdimOut, int *XdimOut)
{
    int x, y, dx, dy;

    float Area, Below;
    int Center;
    int **Data1 = NULL, **Data2 = NULL;
    int max_level = (int)(pow(2,nbits)) - 1;

    /* Allocate input stride array */
    Data1 = (int **)(make_strides(ImageIn, Ydim, Xdim, sizeof(int)));

    /* Allocate output array */
    *ImageOut = (int *)malloc(Ydim*Xdim*sizeof(int));
    Data2 = (int **)(make_strides(*ImageOut, Ydim, Xdim, sizeof(int)));

    /* Was all the memory allocation successful? */
    if (Data1 == NULL || *ImageOut == NULL || Data2 == NULL)
    {
        errno = ENOMEM;
        goto end;
    }

    for (y = 0; y < Ydim; y++)
        for (x = 0; x < Xdim; x++)
        {
            /* Consider neighborhood radius R about point */
            Area = 0.0;
            Below = 0.0;
            Center = Data1[y][x];

            for (dy = -Radius; dy <= Radius; dy+=Step)
                for (dx = -Radius; dx <= Radius; dx+=Step)
                {
                    if ((y + dy >= 0) && (y + dy < Ydim - 1) && (x + dx >= 0) && (x + dx < Xdim - 1))
                    {
                        Area += 1;
                        if (Data1[y + dy][x + dx] < Center)
                            Below += 1;
                    }
                }
            Data2[y][x] = max_level * Below / Area;
        }

end:
    if (Data1 != NULL) free(Data1);
    if (Data2 != NULL) free(Data2);

    *YdimOut = Ydim;
    *XdimOut = Xdim;
}

void parallel_rr(int *ImageIn, int Ydim, int Xdim, int nbits, int Radius, int Step, int **ImageOut, int *YdimOut, int *XdimOut)
{
    int x, y, dx, dy;

    float Area, Below;
    int Center;
    int **Data1 = NULL, **Data2 = NULL;
    int max_level = (int)(pow(2,nbits)) - 1;

    /* Allocate input stride array */
    Data1 = (int **)(make_strides(ImageIn, Ydim, Xdim, sizeof(int)));

    /* Allocate output array */
    *ImageOut = (int *)malloc(Ydim*Xdim*sizeof(int));
    Data2 = (int **)(make_strides(*ImageOut, Ydim, Xdim, sizeof(int)));

    /* Was all the memory allocation successful? */
    if (Data1 == NULL || *ImageOut == NULL || Data2 == NULL)
    {
        errno = ENOMEM;
        goto end;
    }

    #pragma omp parallel for        \
        default(shared) private(x,dy,dx,Area,Below,Center)

    for (y = 0; y < Ydim; y++)
        for (x = 0; x < Xdim; x++)
        {
            /* Consider neighborhood radius R about point */
            Area = 0.0;
            Below = 0.0;
            Center = Data1[y][x];

            for (dy = -Radius; dy <= Radius; dy+=Step)
                for (dx = -Radius; dx <= Radius; dx+=Step)
                {
                    if ((y + dy >= 0) && (y + dy < Ydim - 1) && (x + dx >= 0) && (x + dx < Xdim - 1))
                    {
                        Area += 1;
                        if (Data1[y + dy][x + dx] < Center)
                            Below += 1;
                    }
                }

            Data2[y][x] = max_level * Below / Area;
        }

end:
    if (Data1 != NULL) free(Data1);
    if (Data2 != NULL) free(Data2);

    *YdimOut = Ydim;
    *XdimOut = Xdim;
}
