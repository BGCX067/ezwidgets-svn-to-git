/* 
 * Simple program for testing wrr
 *
 * I used gopt for parsing the arguments.
 * http://www.purposeful.co.uk/software/gopt/
 *
 * I used elapsed as per the stackoverflow recipe:
 * http://stackoverflow.com/questions/2962785/c-using-clock-to-measure-time-in-multi-threaded-programs
 *
 * Note: in terms of pure CPU clock (timed using clock()), the thread creation increase the execution time by 10%
 *
 *
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>
#include <time.h>
#include <errno.h>

#include "gopt.h"
#include "wrr.h"

int main( int argc, const char **argv )
{
    const char *arg;
    float BlurStdDev = 100.0;
    float WeightStdDev = 20.0;
    int Radius = 40;

    int step = 4;
    int repeats = 10;

    int image_size = 512, *image=NULL, *image_out=NULL, image_h, image_w;
    clock_t c0, c1;
    double elapsed, seconds_single=0, seconds_multi=0, clock_single=0, clock_multi=0;;
    struct timespec start, finish;

    int i;

    void *options= gopt_sort( & argc, argv, gopt_start(
        gopt_option( 'h', 0, gopt_shorts( 'h', '?' ), gopt_longs( "help", "HELP" )),
        gopt_option( 's', GOPT_ARG, gopt_shorts( 's' ), gopt_longs( "stddev" )),
        gopt_option( 'r', GOPT_ARG, gopt_shorts( 'r' ), gopt_longs( "radius" )),
        gopt_option( 'b', GOPT_ARG, gopt_shorts( 'b' ), gopt_longs( "blurring" )),
        gopt_option( 'i', GOPT_ARG, gopt_shorts( 'i' ), gopt_longs( "step" )),
        gopt_option( 'n', GOPT_ARG, gopt_shorts( 'n' ), gopt_longs( "repeat" ))));

    if( gopt( options, 'h' ) )
    {
        //if any of the help options was specified
        fprintf( stdout, "This program tests the single and multi-threaded versions of the wrr algorithm\nover a blank image and reports the speed-up achieved.\n\ntest_wrr [options]\n \
    [-s #]  StdDev of weighting Gaussian (%.1f)\n \
    [-r #]  Radius of weighting region (%d)\n \
    [-b #]  StdDev of blurring Gaussian (%.1f)\n \
    [-i #]  Step size (%d)\n \
    [-n #]  Number of repeat tests (%d)\n\n",WeightStdDev, Radius, BlurStdDev, step, repeats);

        exit( EXIT_SUCCESS );
    }

    if( gopt_arg( options, 's', &arg)) WeightStdDev = atof(arg);
    if( gopt_arg( options, 'r', &arg)) Radius = atoi(arg);
    if( gopt_arg( options, 'b', &arg)) BlurStdDev = atof(arg);
    if( gopt_arg( options, 'i', &arg)) step = atoi(arg);
    if( gopt_arg( options, 'n', &arg)) repeats = atoi(arg);

    gopt_free( options );

    //define the blank image
    image = (int *)calloc(image_size*image_size,sizeof(int));

    if (image == NULL)
    {
        fprintf(stderr,"Not enough memory to allocate the image...\n");
        exit( EXIT_FAILURE );
    }

    //single threaded
    printf("\nTesting the single-threaded version:\n");
    for (i=0; i<repeats; i++)
    {
        clock_gettime(CLOCK_MONOTONIC, &start);
        c0 = clock();
        wrr(image, image_size, image_size, 16, BlurStdDev, WeightStdDev, Radius, step, &image_out, &image_h, &image_w);
        c1 = clock();
        clock_gettime(CLOCK_MONOTONIC, &finish);

        if (errno != 0)
            break;

        elapsed = (finish.tv_sec - start.tv_sec);
        elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;

        printf("  iteration %d/%d, %.3fs\n", i+1, repeats, elapsed);
        seconds_single += elapsed;
        clock_single += (c1-c0);

        if (image_out != NULL) free(image_out);
    }

    seconds_single = seconds_single / repeats;
    clock_single = clock_single / repeats;

    if (errno != 0)
    {
        fprintf(stderr,"Something went wrong...\n");
        exit( EXIT_FAILURE );
    }
    printf("  mean for %d repeats: %.3fs\n",repeats, seconds_single);

    //multi-threaded
    printf("\nTesting the multi-threaded version:\n");
    for (i=0; i<repeats; i++)
    {
        clock_gettime(CLOCK_MONOTONIC, &start);
        c0 = clock();
        parallel_wrr(image, image_size, image_size, 16, BlurStdDev, WeightStdDev, Radius, step, &image_out, &image_h, &image_w);
        c1 = clock();
        clock_gettime(CLOCK_MONOTONIC, &finish);

        if (errno != 0)
            break;

        elapsed = (finish.tv_sec - start.tv_sec);
        elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;

        printf("  iteration %d/%d, %.3fs\n", i+1, repeats, elapsed);
        seconds_multi += elapsed;
        clock_multi += (c1-c0);

        if (image_out != NULL) free(image_out);
    }
    seconds_multi = seconds_multi / repeats;
    clock_multi = clock_multi / repeats;

    if (errno != 0)
    {
        fprintf(stderr,"Something went wrong...\n");
        exit( EXIT_FAILURE );
    }
    printf("  mean for %d repeats: %.3fs\n",repeats, seconds_multi);
    printf("\nMulti-threaded version speed-up: %.2fx\n",seconds_single/seconds_multi);
    printf("Thread creation impact: %.2f%%\n", (clock_multi-clock_single)/clock_single*100.);

    if (image != NULL) free(image);

    exit( EXIT_SUCCESS );
}
