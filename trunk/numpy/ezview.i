%module ezview

%{
    #define SWIG_FILE_WITH_INIT
    #include "ezview.h"

    double *my_array = NULL;
    int my_n = 10;

    void __call_at_begining()
    {
        printf("__call_at_begining...\n");
        my_array = (double *)malloc(my_n*sizeof(double));
    }

    void __call_at_end(void)
    {
        printf("__call_at_end...\n");
        if (my_array != NULL)
            free(my_array);
    }
%}

%include "numpy.i"

%init %{
    import_array();
    __call_at_begining();
%}

%apply (double** ARGOUTVIEW_ARRAY1, int *DIM1) {(double** vec, int* n)}

%include "ezview.h"
%rename (set_ones) my_set_ones;

%inline %{
void finalize(void){
    __call_at_end();
}

void get_view(double **vec, int* n) {
    *vec = my_array;
    *n = my_n;
}

void my_set_ones(double **vec, int* n) {
    set_ones(my_array,my_n);
    *vec = my_array;
    *n = my_n;
}
%}

